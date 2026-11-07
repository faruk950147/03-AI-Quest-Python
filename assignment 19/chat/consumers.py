from channels.consumer import AsyncConsumer, SyncConsumer
import asyncio
import json
'''
class ChatConsumer1(AsyncConsumer):
    async def websocket_connect(self, event):
        print("WebSocket connected", event)

        await self.send({
            "type": "websocket.accept"
        })

    async def websocket_receive(self, event):
        print("Message received from WebSocket", event)
        # Loop used because real-time data is sent to the 
        # client every second for 5 seconds
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
'''

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
                "text": str(i),
            })

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
        data = json.loads(event.get("text"))
        self.send({
            "type": "websocket.send",
            "text": json.dumps(data)
        })

    def websocket_disconnect(self, event):
        print("WebSocket disconnected", event)
