from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.utils.http import urlsafe_base64_decode
from django.http import JsonResponse
from django.views import generic
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash, get_backends
from django.db.models import Q
from django.contrib import messages
from validate_email import validate_email
import json
import logging
from account.models import Shipping
from account.forms import (
    SignUpForm, SignInForm, 
    ChangePasswordForm, ResetPasswordForm, 
    ResetPasswordConfirmForm,
    UserForm,
    ShippingForm
)
from account.utilities import (
    account_activation_token, ActivationEmailSender, 
    reset_password_token, ResetPasswordEmailSender
) 
from account.mixing import LoginRequiredMixin, LogoutRequiredMixin

User = get_user_model()
logger = logging.getLogger('project')


# =========================
# Username Validation
# =========================
@method_decorator(never_cache, name='dispatch')
class UsernameValidationView(generic.View):
    def post(self, request):
        data = json.loads(request.body)
        username = data.get('username', '').strip()

        if not username:
            logger.info("Username validation failed: empty input")
            return JsonResponse({'status': 'error', 'message': 'Username cannot be empty'})

        if not username.isalnum():
            logger.info(f"Username validation failed: {username} contains non-alphanumeric characters")
            return JsonResponse({'status': 'error', 'message': 'Username should only contain letters and numbers'})

        if User.objects.filter(username__iexact=username).exists():
            logger.info(f"Username validation failed: {username} already exists")
            return JsonResponse({'status': 'error', 'message': 'This username is already taken'})

        logger.info(f"Username validated successfully: {username}")
        return JsonResponse({'status': 'success', 'message': 'Username is valid and available'})


# =========================
# Email Validation
# =========================
@method_decorator(never_cache, name='dispatch')
class EmailValidationView(generic.View):
    def post(self, request):
        data = json.loads(request.body)
        email = data.get('email', '').strip().lower()

        if not email:
            logger.info("Email validation failed: empty input")
            return JsonResponse({'status': 'error', 'message': 'Email cannot be empty'})

        if not validate_email(email):
            logger.info(f"Email validation failed: {email} is invalid")
            return JsonResponse({'status': 'error', 'message': 'Email is not valid'})

        if User.objects.filter(email__iexact=email).exists():
            logger.info(f"Email validation failed: {email} already in use")
            return JsonResponse({'status': 'error', 'message': 'This email is already in use'})

        logger.info(f"Email validated successfully: {email}")
        return JsonResponse({'status': 'success', 'message': 'Email is valid and available'})


# =========================
# Password Validation
# =========================
@method_decorator(never_cache, name='dispatch')
class PasswordValidationView(generic.View):
    def post(self, request):
        data = json.loads(request.body)
        password = data.get('password', '')
        password2 = data.get('password2', '')

        if password != password2:
            logger.info("Password validation failed: passwords do not match")
            return JsonResponse({'status': 'error', 'message': 'Passwords do not match'})

        if len(password) < 8:
            logger.info("Password validation failed: password too short")
            return JsonResponse({'status': 'error', 'message': 'Password must be at least 8 characters long'})

        logger.info("Password validated successfully")
        return JsonResponse({'status': 'success', 'message': 'Passwords match'})


# =========================
# Sign In Validation
# =========================
@method_decorator(never_cache, name='dispatch')
class SignInValidationView(generic.View):
    def post(self, request):
        data = json.loads(request.body)
        username_or_email = data.get('username', '').strip()

        if not username_or_email:
            logger.info("Sign-in validation failed: empty input")
            return JsonResponse({'status': 'error', 'message': 'Username or email is required'})

        if not User.objects.filter(
            Q(username__iexact=username_or_email) | Q(email__iexact=username_or_email)
        ).exists():
            logger.info(f"Sign-in validation failed: no account found for {username_or_email}")
            return JsonResponse({'status': 'error', 'message': 'No account found with this username or email'})

        logger.info(f"Sign-in validation success: account exists for {username_or_email}")
        return JsonResponse({'status': 'success', 'message': 'Account exists'})


# =========================
# Account Activation
# =========================
@method_decorator(never_cache, name='dispatch')
class AccountActivationView(generic.View):
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode('utf-8')
            user = User.objects.get(id=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist) as e:
            messages.error(request, 'Activation link is invalid.')
            logger.warning(f"Account activation failed: {e}")
            return redirect('sign-in')

        if account_activation_token.check_token(user, token):
            if not user.is_active:
                user.is_active = True
                user.save()
                backend = get_backends()[0].__class__.__module__ + "." + get_backends()[0].__class__.__name__
                login(request, user, backend=backend)
                logger.info(f"Account activated: {user.username} ({user.id})")
                messages.success(request, 'Account activated successfully and signed in.')
            else:
                messages.info(request, 'Account already activated.')
                if not request.user.is_authenticated:
                    backend = get_backends()[0].__class__.__module__ + "." + get_backends()[0].__class__.__name__
                    login(request, user, backend=backend)
                    logger.info(f"Account already active, auto-logged in: {user.username} ({user.id})")
        else:
            messages.error(request, 'Activation link is invalid or expired.')
            logger.warning(f"Account activation failed: invalid/expired token for user {user.username} ({user.id})")

        return redirect('home')


# =========================
# Sign Up
# =========================
@method_decorator(never_cache, name='dispatch')
class SignUpView(LogoutRequiredMixin, generic.View):
    logout = 'sign-in'
    def get(self, request):
        return render(request, 'account/sign-up.html', {'form': SignUpForm()})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.is_active = False
            user.save()
            ActivationEmailSender(user, request).send()
            logger.info(f"New account created (inactive): {user.username} ({user.id})")
            messages.success(request, 'Account created. Check your email to activate your account.')
            return redirect('sign-in')
        logger.info("Sign-up form invalid")
        messages.error(request, 'Correct the errors below.')
        return render(request, 'account/sign-up.html', {'form': form})


# =========================
# Sign In
# =========================
@method_decorator(never_cache, name='dispatch')
class SignInView(LogoutRequiredMixin, generic.View):
    logout = 'sign-in'
    def get(self, request):
        form = SignInForm()
        return render(request, 'account/sign-in.html', {'form': form})

    def post(self, request):
        form = SignInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    logger.info(f"User signed in: {user.username} ({user.id})")
                    messages.success(request, f'Welcome back, {user.username}!')
                    return redirect('home')
                else:
                    messages.error(request, 'Your account is not activated yet.')
                    logger.warning(f"Inactive user attempted sign-in: {user.username} ({user.id})")
            else:
                messages.error(request, 'Invalid username or password.')
                logger.warning(f"Failed sign-in attempt for username: {username}")
        else:
            messages.error(request, 'Please correct the errors below.')
            logger.info("Sign-in form invalid")
        return render(request, 'account/sign-in.html', {'form': form})


# =========================
# Sign Out
# =========================
@method_decorator(never_cache, name='dispatch')
class SignOutView(LoginRequiredMixin, generic.View):
    login_url = 'sign-in'
    def get(self, request):
        logger.info(f"User signed out: {request.user.username} ({request.user.id})")
        logout(request)
        messages.success(request, 'Signed out successfully.')
        return redirect('sign-in')


# =========================
# Change Password
# =========================
@method_decorator(never_cache, name='dispatch')
class ChangesPasswordView(LoginRequiredMixin, generic.View):
    login_url = 'sign-in'

    def get(self, request):
        form = ChangePasswordForm(user=request.user)
        return render(request, 'account/changes-password.html', {'form': form})

    def post(self, request):
        form = ChangePasswordForm(user=request.user, data=request.POST)
        if form.is_valid():
            new_password = form.cleaned_data.get('password')
            request.user.set_password(new_password)
            request.user.save()
            update_session_auth_hash(request, request.user)
            logger.info(f"Password changed for user: {request.user.username} ({request.user.id})")
            logout(request)
            messages.success(request, "Password successfully changed!")
            return redirect('sign-in')
        logger.info(f"Password change failed for user: {request.user.username} ({request.user.id})")
        return render(request, 'account/changes-password.html', {'form': form})


# =========================
# Reset Password
# =========================
@method_decorator(never_cache, name='dispatch')
class ResetPasswordView(LogoutRequiredMixin, generic.View):
    login_url = 'sign-in'
    def get(self, request):
        form = ResetPasswordForm()
        return render(request, 'account/reset-password.html', {'form': form})

    def post(self, request):
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            try:
                user = User.objects.get(email__iexact=email)
                ResetPasswordEmailSender(user, request).send()
                logger.info(f"Password reset email sent to: {email} (user_id={user.id})")
                messages.success(request, "Password reset link has been sent to your email.")
            except User.DoesNotExist:
                logger.warning(f"No user found for password reset: {email}")
                messages.error(request, "No account found with this email.")
            return redirect('reset-password')
        logger.info(f"Password reset form invalid for email: {request.POST.get('email')}")
        return render(request, 'account/reset-password.html', {'form': form})


# =========================
# Reset Password Confirm
# =========================
@method_decorator(never_cache, name='dispatch')
class ResetPasswordConfirmView(LogoutRequiredMixin, generic.View):
    login_url = 'sign-in'

    def get_user_from_uid(self, uidb64):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            return User.objects.get(id=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return None

    def get(self, request, uidb64, token):
        user = self.get_user_from_uid(uidb64)
        if not user or not reset_password_token.check_token(user, token):
            messages.error(request, "Invalid or expired reset link.")
            logger.warning(f"Invalid password reset attempt for UID={uidb64}")
            return redirect('reset-password')
        form = ResetPasswordConfirmForm()
        return render(request, 'account/reset-password-confirm.html', {'form': form})

    def post(self, request, uidb64, token):
        user = self.get_user_from_uid(uidb64)
        if not user or not reset_password_token.check_token(user, token):
            messages.error(request, "Invalid or expired reset link.")
            logger.warning(f"Invalid password reset attempt for UID={uidb64}")
            return redirect('reset-password')
        form = ResetPasswordConfirmForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data.get('password')
            user.set_password(password)
            user.save()
            logger.info(f"Password reset successful for user: {user.username} ({user.id})")
            messages.success(request, "Password reset successful. You can sign in now.")
            return redirect('sign-in')
        return render(request, 'account/reset-password-confirm.html', {'form': form})


# =========================
# User Info Edit
# =========================
@method_decorator(never_cache, name='dispatch')
class UserInfoEditView(LoginRequiredMixin, generic.View):
    login_url = 'sign-in'
    def get(self, request):
        form = UserForm(instance=request.user)
        return render(request, 'account/user-info-edit.html', {'form': form})
    def post(self, request):
        form = UserForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('account')  
        return render(request, 'account/user-info-edit.html', {'form': form})


# =========================
# Shipping Views (Add/Edit/Delete/List)
# =========================
@method_decorator(never_cache, name='dispatch')
class ShippingAddressView(LoginRequiredMixin, generic.View):
    login_url = 'sign-in'
    def get(self, request):
        form = ShippingForm()
        return render(request, 'account/shipping.html', {'form': form})
    def post(self, request):
        form = ShippingForm(request.POST)
        if form.is_valid():
            shipping = form.save(commit=False)
            shipping.user = request.user
            shipping.save()
            messages.success(request, 'Shipping address added successful')
            return redirect('address-list')
        messages.error(request, 'Shipping address added unsuccessful')
        return render(request, 'account/shipping.html', {'form': form})


@method_decorator(never_cache, name='dispatch')
class ShippingAddressListView(LoginRequiredMixin, generic.View):
    login_url = 'sign-in'
    def get(self, request):
        addresses = Shipping.objects.filter(user=request.user)
        return render(request, 'account/address-list.html', {'addresses': addresses})


@method_decorator(never_cache, name='dispatch')
class ShippingAddressDeleteView(LoginRequiredMixin, generic.View):
    login_url = 'sign-in'
    def post(self, request, id):
        shipping = get_object_or_404(Shipping, id=id, user=request.user)
        shipping.delete()
        messages.success(request, "Shipping address deleted successfully.")
        return redirect('address-list')


@method_decorator(never_cache, name='dispatch')
class ShippingAddressEditView(LoginRequiredMixin, generic.View):
    login_url = 'sign-in'
    def get(self, request, id):
        shipping = get_object_or_404(Shipping, id=id, user=request.user)
        form = ShippingForm(instance=shipping)
        return render(request, 'account/shipping-edit.html', {'form': form})
    def post(self, request, id):
        shipping = get_object_or_404(Shipping, id=id, user=request.user)
        form = ShippingForm(request.POST, instance=shipping)
        if form.is_valid():
            form.save()
            return redirect('address-list')
        return render(request, 'account/shipping-edit.html', {'form': form})


# =========================
# Account View
# =========================
@method_decorator(never_cache, name='dispatch')
class AccountView(LoginRequiredMixin, generic.View):
    login_url = 'sign-in'
    def get(self, request):
        return render(request, 'account/account.html')
