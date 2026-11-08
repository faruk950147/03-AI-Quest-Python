from django.urls import path
from chat.consumers import ChatConsumer1

websocket_urlpatterns = [
    path('ws/chat/<str:room_name>/', ChatConsumer1.as_asgi()),
]