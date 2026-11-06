from django.urls import path
from chat.views import HomeView, EmailSendView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('send-email/', EmailSendView.as_view(), name='send-email'),    
]