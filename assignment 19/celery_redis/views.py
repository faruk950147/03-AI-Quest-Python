from django.views import View
from django.shortcuts import render
from django.http import HttpResponse

class HomeView(View):
    def get(self, request):
        return HttpResponse("Hello, this is the Home View!")
    
    def post(self, request):
        # Handle POST request logic here
        return HttpResponse("POST request received")
