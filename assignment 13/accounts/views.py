from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import generic
from accounts.forms import SignUpForm, SignInForm, ChangePasswordForm
from django.contrib.auth import update_session_auth_hash, logout, authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin

# Sign-up View
class SignUpView(generic.View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('profile')
        form = SignUpForm()
        return render(request, 'accounts/sign-up.html', {'form': form})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Account created successfully! Please sign in.')
            return redirect('sign-in')
        messages.error(request, 'Please correct the errors below.')
        return render(request, 'accounts/sign-up.html', {'form': form})

# Sign-in View
""" 
class SignInView(generic.View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('profile')
        form = SignInForm()
        return render(request, 'accounts/sign-in.html', {'form': form})

    def post(self, request):
        # when use authenticationForm use request=request, data=request.POST
        # to pass request object and POST data to the form
        # when use custom form just pass request.POST
  
        form = SignInForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.username}!')
                return redirect('profile')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Please correct the errors below.')

        return render(request, 'accounts/sign-in.html', {'form': form})

# Sign-out View
class SignOutView(LoginRequiredMixin, generic.View):
    # Logs out the user and redirects to the sign-in page with a success message.
    def post(self, request):
        logout(request)
        messages.success(request, 'You have been signed out successfully.')
        return redirect('sign-in')
    
    # Optional: support GET request too (less secure)
    def get(self, request):
        logout(request)
        messages.success(request, 'You have been signed out successfully.')
        return redirect('sign-in')
        

# Password Change View
class PasswordChangeView(generic.View):
    def get(self, request):
        form = ChangePasswordForm(user=request.user)
        return render(request, 'accounts/password-change.html', {'form': form})

    def post(self, request):
        form = ChangePasswordForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Prevent logout after password change
            messages.success(request, 'Password changed successfully.')
            return redirect('profile')
        messages.error(request, 'Please correct the errors below.')
        return render(request, 'accounts/password-change.html', {'form': form})


# Password Reset View
class PasswordResetView(generic.View):
    def get(self, request):
        return render(request, 'accounts/password-reset.html', {})
 """
# Profile View
class ProfileView(LoginRequiredMixin, generic.View):
    def get(self, request):
        return render(request, 'accounts/profile.html', {})
