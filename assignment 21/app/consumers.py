from channels.consumer import AsyncConsumer
import json


class ChatConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        await self.channel_layer.group_add(
            self.room_group_name, self.channel_name
        )

        await self.send({"type": "websocket.accept"})
        print(f"WebSocket Connected: {event}")

    async def websocket_receive(self, event):
        data = json.loads(event["text"])
        message = data.get("message", "")

        # Send message to all users in the group
        await self.channel_layer.group_send(
            self.room_group_name, {
                "type": "chat_message", 
                "message": message
            }
        )
        print(f"WebSocket recieved: {event}")
        
    async def chat_message(self, event):
        await self.send({
                "type": "websocket.send",
                "text": json.dumps({"message": event["message"]}),
            })
        print(f"WebSocket chat messages: {event}")

    async def websocket_disconnect(self, event):
        await self.channel_layer.group_discard(
            self.room_group_name, self.channel_name
        )
        print(f"WebSocket Disconnected: {event}")
