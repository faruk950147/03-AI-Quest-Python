from django.urls import path
from home.views import StudentRegistrationPost, StudentRegistrationGet
urlpatterns = [
    path('', StudentRegistrationPost.as_view(), name = 'StudentRegistrationPost'),
    path('get', StudentRegistrationGet.as_view(), name = 'StudentRegistrationGet')
]
