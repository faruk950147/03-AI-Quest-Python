from django.shortcuts import render
from django.views import generic
# Create your views here.
class TeacherView(generic.View):
    def get(self, request):
        context = {

        }
        return render(request, "teacher/teacher.html", context)

