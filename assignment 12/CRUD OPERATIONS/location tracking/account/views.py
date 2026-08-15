from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from account.forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib import messages
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

class SignUpView(View):
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, 'account/sign-up.html', {'form': form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful.')
            return redirect('sign-in')
        return render(request, 'account/sign-up.html', {'form': form})

class SignInView(View):
    def get(self, request):
        form = CustomAuthenticationForm()
        return render(request, 'account/sign-in.html', {'form': form})

    def post(self, request):
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Login successful.')
                return redirect('map')
        messages.error(request, 'Invalid username or password.')
        return render(request, 'account/sign-in.html', {'form': form})