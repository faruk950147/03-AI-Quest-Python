from django.urls import path
from collage.views import HomeView
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
]