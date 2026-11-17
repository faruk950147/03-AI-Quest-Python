import json

from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async

from chat.models import Messages


class ChatConsumer(AsyncConsumer):
    # Connect WebSocket
    async def websocket_connect(self, event):
        print("Type:", self.scope.get("type"))
        print("Path:", self.scope.get("path"))
        print("Headers:", self.scope.get("headers"))
        print("User:", self.scope.get("user"))
        print("URL Route:", self.scope.get("url_route"))
        print("Session:", self.scope.get("session"))

        print("Channel Layer:", self.channel_layer)
        print("Channel Name:", self.channel_name)
        print("Channel Layer Alias:", self.channel_layer_alias)

        user = self.scope["user"]

        if not user.is_authenticated:
            await self.send({"type": "websocket.close"})
            return

        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.send({"type": "websocket.accept"})

        history = await self.get_chat_history()

        await self.send({
            "type": "websocket.send",
            "text": json.dumps({"type": "chat_history", "messages": history}),
        })

    # Receive WebSocket message
    async def websocket_receive(self, event):

        try:
            user = self.scope["user"]

            data = json.loads(event.get("text", "{}"))
            message = data.get("message", "")

            if not isinstance(message, str) or not message.strip():
                await self.send_error("Message cannot be empty")
                return

            saved_message = await self.save_message(user.id, message.strip())

            await self.channel_layer.group_send(
                self.room_group_name, {"type": "chat.message", "message": saved_message}
            )

        except json.JSONDecodeError:
            await self.send_error("Invalid JSON format")

    # Receive group message
    async def chat_message(self, event):

        await self.send({
            "type": "websocket.send",
            "text": json.dumps(
                {"type": "chat_message", "message": event["message"]}
            ),
        })

    # Get chat history
    @database_sync_to_async
    def get_chat_history(self):

        messages = Messages.objects.select_related("user").order_by("-id")[:5]

        return [
            {
                "id": msg.id,
                "username": msg.user.username,
                "room_name": msg.room_name,
                "content": msg.content,
                "created_at": msg.created_at.isoformat(),
            }
            for msg in reversed(list(messages))
        ]

    # Save message
    @database_sync_to_async
    def save_message(self, user_id, content):

        message = Messages.objects.create(user_id=user_id, content=content)

        return {
            "id": message.id,
            "username": message.user.username,
            "content": message.content,
            "created_at": message.created_at.isoformat(),
        }

    # Send error
    async def send_error(self, error):

        await self.send({
            "type": "websocket.send",
            "text": json.dumps({"type": "error", "error": error}),
        })

    # Disconnect WebSocket
    async def websocket_disconnect(self, event):

        if hasattr(self, "room_group_name"):
            await self.channel_layer.group_discard(
                self.room_group_name, self.channel_name
            )
