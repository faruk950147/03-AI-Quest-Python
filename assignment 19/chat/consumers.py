from channels.consumer import AsyncConsumer, SyncConsumer
import asyncio


class ChatConsumer1(AsyncConsumer):
    async def websocket_connect(self, event):
        print("WebSocket connected", event)

        await self.send({
            "type": "websocket.accept"
        })

    async def websocket_receive(self, event):
        print("Message received from WebSocket", event)
        for i in range(5):
            await self.send({
                "type": "websocket.send", 
                # "text": event.get("text")
                "text": str(i),
            })
            await asyncio.sleep(1)

    async def websocket_disconnect(self, event):
        print("WebSocket disconnected", event)
        
        
class ChatConsumer2(SyncConsumer):
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

