from django.urls import path
from home.views import StudentRegistrationPost, CustomMiddlewareView
urlpatterns = [
    path('', StudentRegistrationPost.as_view(), name = 'StudentRegistrationPost'),
    path('middleware', CustomMiddlewareView.as_view(), name = 'CustomMiddlewareView')
]
