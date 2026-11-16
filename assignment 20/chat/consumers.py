from channels.consumer import AsyncConsumer


class ChatConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print("WebSocket Connected")

        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Join the channel group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        # Accept WebSocket connection
        await self.send({"type": "websocket.accept"})

    async def websocket_receive(self, event):
        message = event.get("text")

        print("Received:", message)

        # Send message to everyone in the room
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat_message", "message": message}
        )

    async def chat_message(self, event):
        # Send group message to WebSocket
        await self.send({"type": "websocket.send", "text": event["message"]})

    async def websocket_disconnect(self, event):
        print("WebSocket Disconnected")

        # Leave the channel group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
