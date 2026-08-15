from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.shortcuts import render

# Create your views here.
class HomeView(View):
    def get(self, request):
        return render(request, 'office/home.html')