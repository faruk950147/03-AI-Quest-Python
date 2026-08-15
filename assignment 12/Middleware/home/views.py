
from django.views import View
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from home.forms import Registration
from home.models import Student

class StudentRegistrationPost(View):

    def get(self, request):
        form = Registration()
        students = Student.objects.all()
        return render(request, 'home.html', {'form': form, 'students': students})

    def post(self, request):
        form = Registration(request.POST)
        if form.is_valid():
            form.save()
            return redirect('StudentRegistrationPost')
        students = Student.objects.all()
        return render(request, 'home.html', {'form': form, 'students': students})


class CustomMiddlewareView(View):
    def get(self, request):
        print("Inside view")
        return HttpResponse("Custom middleware is working!")

