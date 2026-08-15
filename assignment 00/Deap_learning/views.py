from django.shortcuts import render
from django.views import generic

# Create your views here.
class Deap_learning(generic.View):
    def get(self, request):
        return render(request, 'Deap_learning/Deap_learning.html')
