from django.urls import path
from chat.views import HomeView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
]