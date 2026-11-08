from channels.consumer import AsyncConsumer
import json


class ChatConsumer(AsyncConsumer):
    # WebSocket Connection
    async def websocket_connect(self, event):
        print("WebSocket connected:", event)

        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]

        await self.send({
            "type": "websocket.accept"
        })

    # Receive message from client
    async def websocket_receive(self, event):
        print("Message received:", event)
        try:
            data = json.loads(event["text"])
            message = data.get("message", "")

            await self.send({
                "type": "websocket.send", 
                "text": json.dumps({"message": message})
            })
        except json.JSONDecodeError:
            print("Invalid JSON received:", event["text"])

    # Disconnect WebSocket
    async def websocket_disconnect(self, event):
        print("WebSocket disconnected:", event)
