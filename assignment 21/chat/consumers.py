import json
import logging
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
# from chat.models import ChatMessage  

logger = logging.getLogger(__name__)

class ChatConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        """Handle websocket connection"""
        try:
            # Room name directly from URL
            self.room_name = self.scope['url_route']['kwargs']['room_name']
            self.room_group_name = f"chat_{self.room_name}"

            # Join group
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )

            # Accept connection
            await self.send({"type": "websocket.accept"})
            logger.info(f"WebSocket connected: {self.channel_name} in room {self.room_name}")
            
            print('WebSocket connected')
            print('channel name:', self.channel_name)
            print('room name:', self.room_name)
            print('room group name:', self.room_group_name)
            print('scope:==========================', type(self.scope))
            print('scope:==========================', self.scope)

        except Exception as e:
            logger.exception(f"Error connecting websocket: {e}")

    async def websocket_receive(self, event):
        """Receive message from WebSocket"""
        try:
            message_text = event.get("text")
            if not message_text:
                return

            data = json.loads(message_text)
            # Username from authenticated user
            username = self.scope["user"].username if self.scope["user"].is_authenticated else "Anonymous"
            text = data.get("message", "").strip()
            if not text:
                return

            # Optional: Save message to DB
            # await self.save_message(username, text)

            # Broadcast message to group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "username": username,
                    "message": text,
                }
            )

        except Exception as e:
            logger.exception(f"Error processing message: {e}")

    async def chat_message(self, event):
        """Send message to WebSocket client"""
        try:
            await self.send({
                "type": "websocket.send",
                "text": json.dumps({
                    "username": event["username"],
                    "message": event["message"],
                })
            })
        except Exception as e:
            logger.exception(f"Error sending message: {e}")

    async def websocket_disconnect(self, event):
        """Handle websocket disconnect"""
        try:
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )
            logger.info(f"WebSocket disconnected: {self.channel_name}")
        except Exception as e:
            logger.exception(f"Error disconnecting websocket: {e}")

    # Optional DB save method
    # @database_sync_to_async
    # def save_message(self, username, message):
    #     ChatMessage.objects.create(room=self.room_name, username=username, message=message)



    
