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

        print("WebSocket Connected:", self.room_name)

    async def websocket_receive(self, event):

        try:
            data = json.loads(event["text"])
            message = data.get("message", "")

            # Send message to all users in the group
            await self.channel_layer.group_send(
                self.room_group_name, {
                    "type": "chat_message", 
                    "message": message
                }
            )

        except json.JSONDecodeError:
            print("Invalid JSON:", event["text"])

    # Receive group message
    async def chat_message(self, event):

        await self.send({
                "type": "websocket.send",
                "text": json.dumps({"message": event["message"]}),
            })

    async def websocket_disconnect(self, event):

        await self.channel_layer.group_discard(
            self.room_group_name, self.channel_name
        )

        print("WebSocket Disconnected")
