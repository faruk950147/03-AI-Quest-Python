from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('celery_redis.urls')),
    path('admin/', admin.site.urls),
]
