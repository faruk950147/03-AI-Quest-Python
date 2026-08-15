from django.shortcuts import render
from django.views import generic
from home.forms import Registration
# Create your views here.
class StudentRegistrationPost(generic.View):
    def get(self, request):
        context = {'form': Registration()}
        return render(request, 'home.html', context)
    
    def post(self, request):
        form = Registration(request.POST)
        if form.is_valid():
            form.save()
        context = {'form': Registration()}
        return render(request, 'home.html', context)
    
class StudentRegistrationGet(generic.View):
    def get(self, request):
        if request.GET:
            form = Registration(request.GET)
            if form.is_valid():
                form.save()
        context = {'form': Registration()}
        return render(request, 'home.html', context)

