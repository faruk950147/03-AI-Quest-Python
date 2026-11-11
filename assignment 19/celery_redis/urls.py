from django.urls import path

from celery_redis.views import HomeView

urlpatterns = [
    path('', HomeView.as_view(), name='home')
]
