from django.urls import path
from chat.views import HomeView, RoomView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("room/<str:room_name>/", RoomView.as_view(), name="room"),
]
