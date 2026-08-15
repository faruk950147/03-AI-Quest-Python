from django.urls import path
from student.views import StudentListView
urlpatterns = [
    path('', StudentListView.as_view(), name='student-list'),
]
