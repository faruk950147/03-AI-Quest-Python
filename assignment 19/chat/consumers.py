from channels.consumer import SyncConsumer, AsyncConsumer

class ChatConsumer(SyncConsumer):
    def websocket_connect(self, event):
        print("WebSocket connected", event)
        self.send({
            "type": "websocket.accept"
        })

    def websocket_receive(self, event):
        print("Message received from WebSocket", event)
        self.send({
            "type": "websocket.send",
            "text": event.get("text")
        })

    def websocket_disconnect(self, event):
        print("WebSocket disconnected", event)
        
        
class ChatConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print("WebSocket connected", event)
        await self.send({
            "type": "websocket.accept"
        })

    async def websocket_receive(self, event):
        print("Message received from WebSocket", event)
        await self.send({
            "type": "websocket.send",
            "text": event.get("text")
        })

    async def websocket_disconnect(self, event):
        print("WebSocket disconnected", event)  