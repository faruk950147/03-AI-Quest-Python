from django.shortcuts import render
from django.views import generic
# Create your views here.
class TeacherView(generic.View):
    def get(self, request):
        context = {
            "teacher_name": "John Doe",
            "teacher_age": 20,
            "teacher_salary": 5000,
        }
        return render(request, "teacher/teacher.html", context)

