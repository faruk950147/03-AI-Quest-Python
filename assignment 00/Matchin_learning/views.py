from django.shortcuts import render
from django.views import generic
from Matchin_learning.forms import StudentRegistrationForm

# Create your views here.
class StudentRegistrationView(generic.CreateView):
    def get(self, request):
        form = StudentRegistrationForm()
        context = {'form': form}
        return render(request, 'Matchin_learning/Matchin_learning.html', context)
        
