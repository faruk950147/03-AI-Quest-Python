from django.shortcuts import render, redirect
from django.views import View
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.contrib.auth import login, logout, update_session_auth_hash

from account.forms import (
    SignupForm,
    EmailVerificationForm,
    LoginForm,
    ChangePasswordForm,
    PasswordResetRequestForm,
    PasswordResetConfirmForm,
    ResendVerificationEmailForm
)

# ============================ SIGNUP =============================
@method_decorator(never_cache, name="dispatch")
class SignupView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect("home")

        return render(request, "account/signup.html", {"form": SignupForm()})

    def post(self, request):
        form = SignupForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(request, "Signup successful! Check your email for verification.")

            return redirect("verify-email")
        else:
            messages.error(request, "Invalid signup data. Please check your information.")

        return render(request, "account/signup.html", {"form": form})

# ============================ EMAIL VERIFY ===========================
@method_decorator(never_cache, name="dispatch")
class EmailVerifyView(View):
    def get(self, request):

        return render(request, "account/verify.html", {"form": EmailVerificationForm()})

    def post(self, request):
        form = EmailVerificationForm(request.POST)

        if form.is_valid():
            form.save()
            
            messages.success(request, "Email verified successfully!")
            return redirect("home")
        else:
            messages.error(request, "Invalid verification token. Please try again.")

        return render(request, "account/verify.html", {"form": form})

# =========================== LOGIN ===========================
@method_decorator(never_cache, name="dispatch")
class LoginView(View):

    def get(self, request):

        if request.user.is_authenticated:
            return redirect("home")

        return render(request, "account/login.html", {"form": LoginForm()})

    def post(self, request):

        form = LoginForm(request.POST)

        if form.is_valid():

            user = form.cleaned_data["user"]

            login(request, user)

            # remember me
            keep_logged_in = form.cleaned_data.get("keep_logged_in")

            if keep_logged_in:
                request.session.set_expiry(60 * 60 * 24 * 30)  # 30 days
            else:
                request.session.set_expiry(0)  # browser close logout

            messages.success(request, "Login successful!")

            return redirect("home")
        else:
            messages.error(request, "Invalid login credentials. Please try again.")

        return render(request, "account/login.html", {"form": form})

# =========================== LOGOUT ===========================
@method_decorator(never_cache, name="dispatch")
class LogoutView(View):

    def get(self, request):
        logout(request)
        messages.success(request, "Logged out successfully")
        return redirect("login")

# =========================== CHANGE PASSWORD ===========================
@method_decorator(never_cache, name="dispatch")
class ChangePasswordView(View):

    def get(self, request):

        form = ChangePasswordForm(user=request.user)

        return render(request, "account/change_password.html", {"form": form})

    def post(self, request):
        form = ChangePasswordForm(request.user, request.POST)

        if form.is_valid():
            user = form.save()

            update_session_auth_hash(request, user)

            messages.success(request, "Password changed successfully")

            return redirect("home")
        else:
            messages.error(request, "Invalid password change data. Please check your information.")

        return render(request, "account/change_password.html", {"form": form})

# =========================== PASSWORD RESET ===========================
@method_decorator(never_cache, name="dispatch")
class PasswordResetRequestView(View):
    def get(self, request):

        return render(request, "account/reset_request.html", {"form": PasswordResetRequestForm()})

    def post(self, request):

        form = PasswordResetRequestForm(request.POST)

        if form.is_valid():
            
            form.save()
            
            messages.success(request, "If account exists, reset email sent")
            return redirect("login")
        else:
            messages.error(request, "Invalid password reset data. Please check your information.")
        return render(request, "account/reset_request.html", {"form": form})

# =========================== PASSWORD RESET CONFIRM ===========================
@method_decorator(never_cache, name="dispatch")
class PasswordResetConfirmView(View):
    def get(self, request):

        return render(request, "account/reset_confirm.html", {"form": PasswordResetConfirmForm()})

    def post(self, request):
        form = PasswordResetConfirmForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Password reset successful")
            return redirect("login")
        else:
            messages.error(request, "Invalid password reset data. Please check your information.")
        return render(request, "account/reset_confirm.html", {"form": form})

# =========================== RESEND VERIFICATION EMAIL ===========================
@method_decorator(never_cache, name="dispatch")
class ResendVerificationView(View):
    def get(self, request):
        return render(request, "account/resend.html", {"form": ResendVerificationEmailForm()})

    def post(self, request):
        form = ResendVerificationEmailForm(request.POST)

        if form.is_valid():
            result = form.save()

            messages.success(request, result["message"])

            return redirect("login")
        else:
            messages.error(request, "Invalid verification email data. Please check your information.")
        return render(request, "account/resend.html", {"form": form})
    
class ProfileView(View):
    def get(self, request):
        return render(request, "account/profile.html")