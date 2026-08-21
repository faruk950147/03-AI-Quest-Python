from django.urls import path

from contact.views import (
    ContactView
)

urlpatterns = [
    path('contact/me/', ContactView.as_view(), name='contact')
]
