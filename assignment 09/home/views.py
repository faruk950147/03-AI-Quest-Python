from django.shortcuts import render
from django.views import generic
from home.forms import Registration
# Create your views here.
class HomeView(generic.View):
    def get(self, request):
        
        return render(request, 'home/home.html')
    
    
class RegistrationView(generic.View):
    def get(self, request):
        # auto_id=True for default auto_id generation
        # form = Registration(auto_id=True) 
        # auto_id=False to disable auto_id generation
        form = Registration(auto_id=False)
        # Custom auto_id prefix for form fields id customization
        # form = Registration(auto_id='id_%s') 
        
        return render(request, 'home/registration.html', {'form': form})
    
    def post(self, request):
        form = Registration(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            roll = form.cleaned_data['roll']
            department = form.cleaned_data['department']
            email = form.cleaned_data['email']
            dob = form.cleaned_data['dob']
            gender = form.cleaned_data['gender']
            agree = form.cleaned_data['agree']
            context = {
                'name': name,
                'roll': roll,
                'department': department,
                'email': email,
                'dob': dob,
                'gender': gender,
                'agree': agree
            }
            return render(request, 'home/success.html', context)
        return render(request, 'home/registration.html', {'form': form})
