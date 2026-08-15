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
# Sign-up View
@method_decorator(never_cache, name='dispatch')
class SignUpView(LogoutRequiredMixin, generic.View):
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
@method_decorator(never_cache, name='dispatch')
class SignInView(LogoutRequiredMixin, generic.View):
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

# Password Reset View
@method_decorator(never_cache, name='dispatch')
class PasswordResetView(LogoutRequiredMixin, generic.View):
    def get(self, request):
        return render(request, 'accounts/password-reset.html', {})

# Password Reset Done View
class PasswordResetDoneView(LogoutRequiredMixin, generic.View):
    def get(self, request):
        return render(request, 'accounts/password-reset-done.html', {})

# Password Reset Confirm View
class PasswordResetConfirmView(LogoutRequiredMixin, generic.View):
    def get(self, request):
        return render(request, 'accounts/password-reset-confirm.html', {})

# Password Reset Complete View
class PasswordResetCompleteView(LogoutRequiredMixin, generic.View):
    def get(self, request):
        return render(request, 'accounts/password-reset-complete.html', {})

# Sign-out View
@method_decorator(never_cache, name='dispatch')
class SignOutView(LoginRequiredMixin, generic.View):
    login_url = reverse_lazy('sign-in')
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
            update_session_auth_hash(request, user)  # Prevent logout after password change
            messages.success(request, 'Password changed successfully.')
            return redirect('profile')
        messages.error(request, 'Please correct the errors below.')
        return render(request, 'accounts/password-change.html', {'form': form})


    def get(self, request):
        return render(request, 'accounts/password-reset.html', {})
 """
# Profile View
@method_decorator(never_cache, name='dispatch')
class ProfileView(LoginRequiredMixin, generic.View):
    login_url = reverse_lazy('sign-in')
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('sign-in')
        form = ProfileForm()
        return render(request, 'accounts/profile.html', {'form': form, 'active': 'btn-success'})
    def post(self, request):
        form = ProfileForm(request.POST)
        if form.is_valid():
            # profiles = Profile(
            #     user=request.user,
            #     name = form.cleaned_data['name'],
            #     division=form.cleaned_data['division'],
            #     district=form.cleaned_data['district'],
            #     thana=form.cleaned_data['thana'],
            #     villorroad=form.cleaned_data['villorroad'],
            #     phone=form.cleaned_data['phone'],
            #     zipcode=form.cleaned_data['zipcode'],
            # )
            # profiles.save() 
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
            messages.success(request, 'Profile successfully updated')
        else:
            messages.error(request, 'Something is invalid')
        return render(request, 'accounts/profile.html', {'form': form, 'active': 'btn-success'})

@method_decorator(never_cache, name='dispatch')
class AddressView(LoginRequiredMixin, generic.View):
    login_url = reverse_lazy('sign-in')
    def get(self, request):
        profiles = Profile.objects.filter(user=request.user)
        return render(request, 'accounts/address.html', {'profiles': profiles, 'active': 'btn-success'})