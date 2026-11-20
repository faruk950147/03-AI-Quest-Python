import json

from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async

from chat.models import Messages


class ChatConsumer(AsyncConsumer):
    # Handle WebSocket Connection
    async def websocket_connect(self, event):

        user = self.scope["user"]

        if not user.is_authenticated:
            await self.send({"type": "websocket.close"})
            return

        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.send({"type": "websocket.accept"})

        # Get Chat History
        history = await self.get_chat_history()

        await self.send(
            {
                "type": "websocket.send",
                "text": json.dumps({"type": "chat_history", "messages": history}),
            }
        )

    # Handle Incoming Messages
    async def websocket_receive(self, event):

        try:
            user = self.scope["user"]

            data = json.loads(event.get("text") or "{}")

            message = data.get("message", "")

            if not isinstance(message, str) or not message.strip():
                await self.send_error("Message cannot be empty")
                return

            message = message.strip()

            if len(message) > 2000:
                await self.send_error("Message is too long")
                return

            # Save Message
            saved_message = await self.save_message(user.id, self.room_name, message)

            # Broadcast Message
            await self.channel_layer.group_send(
                self.room_group_name, {"type": "chat.message", "message": saved_message}
            )

        except json.JSONDecodeError:
            await self.send_error("Invalid JSON format")

    # Handle Group Messages
    async def chat_message(self, event):

        await self.send(
            {
                "type": "websocket.send",
                "text": json.dumps(
                    {"type": "chat_message", "message": event["message"]}
                ),
            }
        )

    # Get Chat History
    @database_sync_to_async
    def get_chat_history(self):

        messages = Messages.last_5_messages(self.room_name)

        return [
            {
                "id": msg.id,
                "user_id": msg.user_id,
                "username": msg.user.username,
                "room_name": msg.room_name,
                "content": msg.content,
                "created_at": msg.created_at.strftime("%I:%M %p"),
            }
            for msg in reversed(list(messages))
        ]

    # Save Message
    @database_sync_to_async
    def save_message(self, user_id, room_name, content):

        message = Messages.objects.create(
            user_id=user_id, room_name=room_name, content=content
        )

        return {
            "id": message.id,
            "user_id": message.user_id,
            "username": message.user.username,
            "room_name": message.room_name,
            "content": message.content,
            "created_at": message.created_at.strftime("%I:%M %p"),
        }

    # Send Error
    async def send_error(self, error):

        await self.send(
            {
                "type": "websocket.send",
                "text": json.dumps({"type": "error", "error": error}),
            }
        )

    # Handle WebSocket Disconnect
    async def websocket_disconnect(self, event):

        if hasattr(self, "room_group_name"):
            await self.channel_layer.group_discard(
                self.room_group_name, self.channel_name
            )


class ChatConsumer(AsyncConsumer):

    # Handle WebSocket Connection
    async def websocket_connect(self, event):

        user = self.scope["user"]

        if not user.is_authenticated:
            await self.send({"type": "websocket.close"})
            return

        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.send({"type": "websocket.accept"})

        # Get Chat History
        history = await self.get_chat_history()

        await self.send({
            "type": "websocket.send",
            "text": json.dumps({
                "type": "chat_history",
                "messages": history
            })
        })


    # Handle Incoming Messages
    async def websocket_receive(self, event):

        try:

            user = self.scope["user"]

            data = json.loads(event.get("text") or "{}")

            message = data.get("message", "")

            if not isinstance(message, str) or not message.strip():
                await self.send_error("Message cannot be empty")
                return

            message = message.strip()

            if len(message) > 2000:
                await self.send_error("Message is too long")
                return

            # Save Message
            saved_message = await self.save_message(
                user.id,
                self.room_name,
                message
            )

            # Broadcast Message
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat.message",
                    "message": saved_message
                }
            )

        except json.JSONDecodeError:

            await self.send_error("Invalid JSON format")


    # Handle Group Messages
    async def chat_message(self, event):

        await self.send({
            "type": "websocket.send",
            "text": json.dumps({
                "type": "chat_message",
                "message": event["message"]
            })
        })


    # Get Chat History
    @database_sync_to_async
    def get_chat_history(self):

        messages = Messages.last_5_messages(self.room_name)

        return [
            {
                "id": msg.id,
                "user_id": msg.user_id,
                "username": msg.user.username,
                "room_name": msg.room_name,
                "content": msg.content,
                "created_at": msg.created_at.strftime("%I:%M %p")
            }
            for msg in reversed(list(messages))
        ]


    # Save Message
    @database_sync_to_async
    def save_message(self, user_id, room_name, content):

        message = Messages.objects.create(
            user_id=user_id,
            room_name=room_name,
            content=content
        )

        return {
            "id": message.id,
            "user_id": message.user_id,
            "username": message.user.username,
            "room_name": message.room_name,
            "content": message.content,
            "created_at": message.created_at.strftime("%I:%M %p")
        }


    # Send Error
    async def send_error(self, error):

        await self.send({
            "type": "websocket.send",
            "text": json.dumps({
                "type": "error",
                "error": error
            })
        })


    # Handle WebSocket Disconnect
    async def websocket_disconnect(self, event):

        if hasattr(self, "room_group_name"):

            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )
