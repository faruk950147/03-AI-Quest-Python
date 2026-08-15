from django.shortcuts import render
from django.views import generic

# Create your views here.
class HomeView(generic.View):
    def get(self, request):
        context = {
            "title": "Python Django",
            "department": "CSE",
            "age": 22,
        }
        return render(request, 'collage/home.html', context)
