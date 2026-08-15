from django.shortcuts import render
from django.views import generic
# Create your views here.
class StudentView(generic.View):
    def get(self, request):
        context = {

        }
        return render(request, "student/student.html", context)

