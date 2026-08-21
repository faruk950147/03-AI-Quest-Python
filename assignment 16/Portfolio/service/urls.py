from django.urls import path

from service.views import (
    ServiceView,
)

urlpatterns = [
    path('service/', ServiceView.as_view(), name='service'),
]
