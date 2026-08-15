from django.urls import path
from queryset.views import StudentRegistrationPost
urlpatterns = [
    path('', StudentRegistrationPost.as_view(), name = 'StudentRegistrationPost'),
]
