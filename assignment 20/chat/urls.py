from django.urls import path
from chat.views import ChatView

urlpatterns = [
    path('chat/<str:room_name>/', ChatView.as_view(), name='chat'),
]