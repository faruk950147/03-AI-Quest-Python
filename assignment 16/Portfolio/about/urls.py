from django.urls import path

from about.views import (
    AboutView
)

urlpatterns = [
    path('about/me', AboutView.as_view(), name='about')
]
