from django.shortcuts import render
from django.views import generic
# Create your views here.
class StudentView(generic.View):
    def get(self, request):
        context = {
            "student_name": "John Doe",
            "student_age": 20,
            "student_roll":501,
        }
        return render(request, "student/student.html", context)

