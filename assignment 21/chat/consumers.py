from channels.consumer import AsyncConsumer
import json

class ChatConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        """
        Called when a WebSocket connection is opened.
        All clients join the same fixed group "chat".
        """
        self.group_name = "chat"

        # Join the fixed chat group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        # Accept the WebSocket connection
        await self.send({
            "type": "websocket.accept"
        })
        print(f"{self.channel_name} connected to {self.group_name}")

    async def websocket_receive(self, event):
        """
        Called when a message is received from the WebSocket.
        Expects a JSON object like {"message": "text"}.
        """
        text_data = event.get("text")
        if not text_data:
            return

        try:
            data = json.loads(text_data)
            message = data.get("message")
        except (json.JSONDecodeError, TypeError):
            return

        if message:
            # Broadcast the message to the group
            await self.channel_layer.group_send(
                self.group_name,
                {
                    "type": "chat.message",  # will call `chat_message`
                    "message": message
                }
            )

    async def chat_message(self, event):
        """
        Called by group_send to send message to all clients in the group.
        """
        message = event["message"]

        # Send message to WebSocket client
        await self.send({
            "type": "websocket.send",
            "text": json.dumps({"message": message})
        })

    async def websocket_disconnect(self, event):
        """
        Called when the WebSocket disconnects.
        Removes the client from the group.
        """
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )
        print(f"{self.channel_name} disconnected from {self.group_name}")

'''
from channels.consumer import AsyncConsumer
import json

class ChatConsumer(AsyncConsumer):

    async def websocket_connect(self, event):
        user = self.scope["user"]

        # if user is not authenticated, close the connection
        if user.is_anonymous:
            await self.close()
        else:
            await self.send({"type": "websocket.accept"})

            # group join
            await self.channel_layer.group_add(
                "chat",
                self.channel_name
            )

            print("User connected:", user.username)


    async def websocket_receive(self, event):
        user = self.scope["user"]

        data = json.loads(event.get("text", ""))

        message = data.get("message", "")

        print(f"{user.username} says:", message)

        await self.channel_layer.group_send(
            "chat",
            {
                "type": "chat.message",
                "user": user.username,
                "text": message
            }
        )


    async def websocket_disconnect(self, event):
        print("Disconnected:", self.scope["user"])

        await self.channel_layer.group_discard(
            "chat",
            self.channel_name
        )


    async def chat_message(self, event):
        await self.send({
            "type": "websocket.send",
            "text": json.dumps({
                "user": event["user"],
                "message": json.dumps(event["text"])
            })
        })

'''