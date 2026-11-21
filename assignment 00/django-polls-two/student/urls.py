from django.urls import path
from student.views import HomeView, VotingView, QuestionView, DepartmentView, StudentView

app_name = 'student'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('questions/<int:pk>/voting/', VotingView.as_view(), name='voting'),
    path('questions/<int:pk>/', QuestionView.as_view(), name='questions'),
    path('departments/<int:pk>/', DepartmentView.as_view(), name='departments'),
    path('students/<int:pk>/', StudentView.as_view(), name='students'),
]
