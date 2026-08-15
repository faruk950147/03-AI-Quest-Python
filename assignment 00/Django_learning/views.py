from django.shortcuts import render
from django.views import generic


# Create your views here.
class DjangoLearningView(generic.View):
    def get(self, request):
        context = {
            'machine_learning': 'Machine Learning',
            'Deap_learning': 'Deap Learning',
            'django_learning': 'Django Learning',
            'age': 20,
        }   
        return render(request, 'Django_learning/home.html', context)