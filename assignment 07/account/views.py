from django.shortcuts import render
from django.views import generic
from account.forms import SignUpForm, SignInForm

# Create your views here.
class SignUpView(generic.View):
    def get(self, request):
        return render(request, 'account/signup.html', {'form': SignUpForm()})
        
    def post(self, request):
        pass

class SignInView(generic.View):
    def get(self, request):
        return render(request, 'account/signin.html', {'form': SignInForm()})
        
    def post(self, request):
        pass