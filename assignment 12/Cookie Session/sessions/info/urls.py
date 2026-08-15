from django.urls import path
from .views import SetSession, GetSession, ClearSession

urlpatterns = [
    path('set-session/', SetSession.as_view()),
    path('get-session/', GetSession.as_view()),
    path('clear-session/', ClearSession.as_view()),
]
