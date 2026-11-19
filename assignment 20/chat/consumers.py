import json

from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async

from chat.models import Messages


class ChatConsumer(AsyncConsumer):
    # Handle a new WebSocket connection
    async def websocket_connect(self, event):

        # Display the connection type
        print("Type:", self.scope.get("type"))

        # Display the requested URL path
        print("Path:", self.scope.get("path"))

        # Display the request headers
        print("Headers:", self.scope.get("headers"))

        # Display the currently connected user
        print("User:", self.scope.get("user"))

        # Display URL routing information
        print("URL Route:", self.scope.get("url_route"))

        # Display the current user session
        print("Session:", self.scope.get("session"))

        # Display the configured channel layer
        print("Channel Layer:", self.channel_layer)

        # Display the unique channel name
        print("Channel Name:", self.channel_name)

        # Display the channel layer alias
        print("Channel Layer Alias:", self.channel_layer_alias)

        # Get the currently connected user
        user = self.scope["user"]

        # Check whether the user is authenticated
        if not user.is_authenticated:
            # Close the WebSocket connection
            await self.send({"type": "websocket.close"})
            return

        # Get the room name from the URL parameters
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]

        # Generate a unique group name for the chat room
        self.room_group_name = f"chat_{self.room_name}"

        # Add the current connection to the chat group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        # Accept the WebSocket connection
        await self.send({"type": "websocket.accept"})

        # Retrieve previous chat messages from the database
        history = await self.get_chat_history()

        # Send chat history to the connected client
        await self.send(
            {
                "type": "websocket.send",
                "text": json.dumps({"type": "chat_history", "messages": history}),
            }
        )

    # Handle incoming WebSocket messages
    async def websocket_receive(self, event):

        try:
            # Get the currently connected user
            user = self.scope["user"]

            # Convert the received JSON string into a Python dictionary
            data = json.loads(event.get("text") or "{}")

            # Extract the message content
            message = data.get("message", "")

            # Validate the message type and check whether it is empty
            if not isinstance(message, str) or not message.strip():
                # Send an error response
                await self.send_error("Message cannot be empty")
                return

            # Remove unnecessary whitespace
            message = message.strip()

            # Save the received message into the database
            saved_message = await self.save_message(user.id, self.room_name, message)

            # Broadcast the message to all connections in the chat group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    # Specify the event handler to execute
                    "type": "chat.message",
                    # Pass the saved message data
                    "message": saved_message,
                },
            )

        # Handle invalid JSON data
        except json.JSONDecodeError:
            # Send an invalid JSON error response
            await self.send_error("Invalid JSON format")

    # Handle messages received from the chat group
    async def chat_message(self, event):

        # Send the group message to the connected client
        await self.send(
            {
                "type": "websocket.send",
                "text": json.dumps(
                    {"type": "chat_message", "message": event["message"]}
                ),
            }
        )

    # Retrieve chat history from the database
    @database_sync_to_async
    def get_chat_history(self):

        # Retrieve the latest five messages for the current room
        messages = Messages.last_5_messages(self.room_name)

        # Convert database objects into a list of dictionaries
        return [
            {
                # Get the unique message ID
                "id": msg.id,
                # Get the username of the message sender
                "username": msg.user.username,
                # Get the chat room name
                "room_name": msg.room_name,
                # Get the message content
                "content": msg.content,
                # Convert the timestamp into ISO 8601 format
                "created_at": msg.created_at.isoformat(),
            }
            # Reverse messages to display them from oldest to newest
            for msg in reversed(list(messages))
        ]

    # Save a new message into the database
    @database_sync_to_async
    def save_message(self, user_id, room_name, content):

        # Create a new message record
        message = Messages.objects.create(
            user_id=user_id, room_name=room_name, content=content
        )

        # Return the saved message as a dictionary
        return {
            # Get the newly created message ID
            "id": message.id,
            # Get the sender's username
            "username": message.user.username,
            # Get the chat room name
            "room_name": message.room_name,
            # Get the saved message content
            "content": message.content,
            # Convert the creation timestamp into ISO 8601 format
            "created_at": message.created_at.isoformat(),
        }

    # Send error messages to the client
    async def send_error(self, error):

        # Send the error response through WebSocket
        await self.send(
            {
                "type": "websocket.send",
                # Convert the error information into JSON format
                "text": json.dumps({"type": "error", "error": error}),
            }
        )

    # Handle WebSocket disconnection
    async def websocket_disconnect(self, event):

        # Check whether the room group name exists
        if hasattr(self, "room_group_name"):
            # Remove the current connection from the chat group
            await self.channel_layer.group_discard(
                self.room_group_name, self.channel_name
            )
