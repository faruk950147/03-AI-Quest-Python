from channels.consumer import AsyncConsumer
import json
from chat.models import Messages

class ChatConsumer(AsyncConsumer):
    # connect to websocket
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
        
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.send({"type": "websocket.accept"})

    # Receive message from WebSocket
    async def websocket_receive(self, event):
        try:
            data = json.loads(event.get("text", "{}"))
            message = data.get("message")

            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name, {"type": "chat_message", "message": message}
            )

        except json.JSONDecodeError:
            await self.send(
                {
                    "type": "websocket.send",
                    "text": json.dumps({"error": "Invalid JSON format"}),
                }
            )

    # Receive message from room group
    async def chat_message(self, event):
        # Send message to WebSocket
        await self.send(
            {
                "type": "websocket.send",
                "text": json.dumps({"message": event["message"]}),
            }
        )

    # disconnect to websocket
    async def websocket_disconnect(self, event):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
