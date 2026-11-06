from channels.consumer import SyncConsumer

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