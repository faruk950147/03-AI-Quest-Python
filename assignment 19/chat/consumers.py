from channels.consumer import AsyncConsumer, SyncConsumer


class ChatConsumer1(AsyncConsumer):
    async def connect(self, event):
        print("WebSocket connected", event)
        await self.send({"type": "websocket.accept"})

    async def receive(self, event):
        print("Message received from WebSocket", event)
        await self.send({"type": "websocket.send", "text": event.get("text")})

    async def disconnect(self, event):
        print("WebSocket disconnected", event)
        
        
class ChatConsumer2(SyncConsumer):
    def connect(self, event):
        print("WebSocket connected", event)
        self.send({
            "type": "websocket.accept"
        })

    def receive(self, event):
        print("Message received from WebSocket", event)
        self.send({
            "type": "websocket.send",
            "text": event.get("text")
        })

    def disconnect(self, event):
        print("WebSocket disconnected", event)

