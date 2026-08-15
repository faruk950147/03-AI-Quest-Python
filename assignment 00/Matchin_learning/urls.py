from django.urls import path
from Matchin_learning.views import StudentRegistrationView

urlpatterns = [
    path('', StudentRegistrationView.as_view(), name='student_registration'),
]
