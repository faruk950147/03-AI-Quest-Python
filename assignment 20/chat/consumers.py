from channels.consumer import AsyncConsumer


class ChatConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print("WebSocket Connected")

        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        await self.channel_layer.group_add(
            self.room_group_name, self.channel_name
        )

        await self.send({
            "type": "websocket.accept"
        })

    async def websocket_receive(self, event):
        message = event.get("text")

        print("Received:", message)

        await self.send({
            "type": "websocket.send", 
            "text": message
        })

    async def websocket_disconnect(self, event):
        print("WebSocket Disconnected")
