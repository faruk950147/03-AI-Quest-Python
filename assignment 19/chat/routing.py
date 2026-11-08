from django.urls import path
from chat.consumers import ChatConsumer1, ChatConsumer2

websocket_urlpatterns = [
    path('ws/chat/<str:room_name>/', ChatConsumer1.as_asgi()),
    path('ws/chat2/', ChatConsumer2.as_asgi())
]