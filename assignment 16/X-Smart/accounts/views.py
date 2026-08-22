import logging
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.views import generic
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from accounts.forms import SignUpForm, SignInForm, ChangePasswordForm, ResetPasswordForm, SetNewPasswordForm, ProfileForm
from django.contrib.auth import update_session_auth_hash, logout, authenticate, login
from accounts.models import Profile
from accounts.mixing import LoginRequiredMixin, LogoutRequiredMixin

logger = logging.getLogger('project')


# Sign-up View
@method_decorator(never_cache, name='dispatch')
class SignUpView(LogoutRequiredMixin, generic.View):
    def get(self, request):
        if request.user.is_authenticated:
            logger.info(f"Authenticated user '{request.user}' tried to access sign-up page.")
            return redirect('profile')
        form = SignUpForm()
        logger.info("Anonymous user accessed sign-up page.")
        return render(request, 'accounts/sign-up.html', {'form': form})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            logger.info(f"New user '{user.username}' created successfully.")
            messages.success(request, 'Account created successfully! Please sign in.')
            return redirect('sign-in')
        logger.warning(f"Sign-up form submission failed: {form.errors.as_json()}")
        messages.error(request, 'Please correct the errors below.')
        return render(request, 'accounts/sign-up.html', {'form': form})

# Sign-in View
@method_decorator(never_cache, name='dispatch')
class SignInView(LogoutRequiredMixin, generic.View):
    def get(self, request):
        if request.user.is_authenticated:
            logger.info(f"Authenticated user '{request.user}' tried to access sign-in page.")
            return redirect('profile')
        form = SignInForm()
        logger.info("Anonymous user accessed sign-in page.")
        return render(request, 'accounts/sign-in.html', {'form': form})

    def post(self, request):
        form = SignInForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                logger.info(f"User '{username}' logged in successfully.")
                messages.success(request, f'Welcome back, {user.username}!')
                return redirect('profile')
            else:
                logger.warning(f"Failed login attempt for username '{username}'.")
                messages.error(request, 'Invalid username or password.')
        else:
            logger.warning(f"Sign-in form invalid: {form.errors.as_json()}")
            messages.error(request, 'Please correct the errors below.')
        return render(request, 'accounts/sign-in.html', {'form': form})

# Sign-out View
@method_decorator(never_cache, name='dispatch')
class SignOutView(LoginRequiredMixin, generic.View):
    login_url = reverse_lazy('sign-in')

    def post(self, request):
        logger.info(f"User '{request.user}' logged out via POST.")
        logout(request)
        messages.success(request, 'You have been signed out successfully.')
        return redirect('sign-in')
    
    def get(self, request):
        logger.info(f"User '{request.user}' logged out via GET (less secure).")
        logout(request)
        messages.success(request, 'You have been signed out successfully.')
        return redirect('sign-in')

# Password Change View
"""
@method_decorator(never_cache, name='dispatch')
class PasswordChangeView(LoginRequiredMixin, generic.View):
    login_url = reverse_lazy('sign-in')

    def get(self, request):
        form = ChangePasswordForm(user=request.user)
        return render(request, 'accounts/password-change.html', {'form': form})

    def post(self, request):
        form = ChangePasswordForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            logger.info(f"User '{user.username}' changed password successfully.")
            messages.success(request, 'Password changed successfully.')
            return redirect('profile')
        logger.warning(f"Password change form errors for user '{request.user}': {form.errors.as_json()}")
        messages.error(request, 'Please correct the errors below.')
        return render(request, 'accounts/password-change.html', {'form': form})
 """
# Profile View
@method_decorator(never_cache, name='dispatch')
class ProfileView(LoginRequiredMixin, generic.View):
    login_url = reverse_lazy('sign-in')

    def get(self, request):
        form = ProfileForm()
        return render(request, 'accounts/profile.html', {'form': form, 'active': 'btn-success'})

    def post(self, request):
        form = ProfileForm(request.POST)
        if form.is_valid():
            # update_or_create profile
            Profile.objects.create(
                user=request.user,
                name=form.cleaned_data['name'],
                division=form.cleaned_data['division'],
                district=form.cleaned_data['district'],
                thana=form.cleaned_data['thana'],
                villorroad=form.cleaned_data['villorroad'],
                phone=form.cleaned_data['phone'],
                zipcode=form.cleaned_data['zipcode'],
            )
            logger.info(f"Profile updated for user '{request.user}'.")
            messages.success(request, 'Profile successfully updated')
        else:
            logger.warning(f"Profile update failed for user '{request.user}': {form.errors.as_json()}")
            messages.error(request, 'Something is invalid')
        return render(request, 'accounts/profile.html', {'form': form, 'active': 'btn-success'})

# Address View
@method_decorator(never_cache, name='dispatch')
class AddressView(LoginRequiredMixin, generic.View):
    login_url = reverse_lazy('sign-in')

    def get(self, request):
        profiles = Profile.objects.filter(user=request.user)
        logger.info(f"User '{request.user}' accessed address view. {profiles.count()} profiles found.")
        return render(request, 'accounts/address.html', {'profiles': profiles, 'active': 'btn-success'})
