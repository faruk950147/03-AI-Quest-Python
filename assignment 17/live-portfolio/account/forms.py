import re
from typing import Any
from django import forms
from django.db import transaction
from django.contrib.auth import authenticate, get_user_model, update_session_auth_hash

from account.services import OTPService
from account.tasks import send_verification_email, send_password_reset_email

User = get_user_model()


# ========================= PASSWORD VALIDATION =========================
def validate_password_strength(password: str) -> str:
    if not password:
        raise forms.ValidationError("Password is required.")
    if len(password) < 8:
        raise forms.ValidationError("Password must be at least 8 characters.")
    if not re.search(r"[A-Z]", password):
        raise forms.ValidationError("Password must contain at least one uppercase letter.")
    if not re.search(r"[a-z]", password):
        raise forms.ValidationError("Password must contain at least one lowercase letter.")
    if not re.search(r"\d", password):
        raise forms.ValidationError("Password must contain at least one number.")
    return password


# ========================= BASE STYLED FORM =========================
class StyledForm(forms.Form):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            if isinstance(
                field.widget,
                (
                    forms.TextInput,
                    forms.PasswordInput,
                    forms.EmailInput,
                    forms.NumberInput,
                    forms.Textarea,
                ),
            ):
                field.widget.attrs.setdefault("class", "form-control")


# ========================= SIGNUP FORM =======================
class SignupForm(forms.ModelForm, StyledForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Your Password"}),
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Confirm Your Password"}),
    )

    class Meta:
        model = User
        fields = ["username", "email", "phone", "password"]
        widgets = {
            "username": forms.TextInput(attrs={"placeholder": "Your username"}),
            "email": forms.EmailInput(attrs={"placeholder": "Your email"}),
            "phone": forms.TextInput(attrs={"placeholder": "Your phone number"}),
        }

    def clean_username(self) -> str:
        username = self.cleaned_data.get("username", "").strip().lower()
        if username and User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError("Username already exists.")
        return username

    def clean_email(self) -> str:
        email = self.cleaned_data.get("email", "").strip().lower()
        if email and User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Email already exists.")
        return email

    def clean_phone(self) -> str | None:
        phone = self.cleaned_data.get("phone")
        if phone and User.objects.filter(phone=phone).exists():
            raise forms.ValidationError("Phone number already exists.")
        return phone

    def clean(self) -> dict[str, Any]:
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")

        if password and password2:
            if password != password2:
                self.add_error("password2", "Passwords do not match.")
            else:
                try:
                    validate_password_strength(password)
                except forms.ValidationError as error:
                    self.add_error("password", error)

        return cleaned_data

    def save(self, commit: bool = True) -> User:
        user = super().save(commit=False)
        password = self.cleaned_data.get("password")
        if password:
            user.set_password(password)

        user.is_active = False
        user.is_verified = False

        if commit:
            with transaction.atomic():
                user.save()
                email = user.email
                otp = OTPService.generate()
                OTPService.save(email, otp)
                transaction.on_commit(lambda e=email, o=otp: send_verification_email.delay(e, o))

        return user


# ========================= VERIFY EMAIL =======================
class VerifyEmailForm(StyledForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"placeholder": "Your Email"}),
    )
    otp = forms.CharField(
        min_length=6,
        max_length=6,
        widget=forms.TextInput(attrs={
            "placeholder": "Your 6-digit OTP",
            "maxlength": "6"
        })
    )

    def clean(self) -> dict[str, Any]:
        cleaned_data = super().clean()

        email = cleaned_data.get("email")
        otp = cleaned_data.get("otp")

        if not email or not otp:
            return cleaned_data

        email = email.strip().lower()
        user = User.objects.filter(email__iexact=email).first()

        if user is None:
            self.add_error("email", "User does not exist.")
            return cleaned_data

        if user.is_verified:
            self.add_error("email", "Email is already verified.")
            return cleaned_data

        if not OTPService.verify(user.email, otp):
            self.add_error("otp", "Invalid or expired OTP.")
            return cleaned_data

        self.user = user
        return cleaned_data

    def save(self, commit: bool = True) -> User:
        user = getattr(self, "user", None)
        if not user:
            raise ValueError("Cannot save form without valid user.")

        user.is_verified = True
        user.is_active = True

        if commit:
            with transaction.atomic():
                user.save(update_fields=["is_verified", "is_active"])

        return user


# ========================= LOGIN FORM =========================
class LoginForm(StyledForm):
    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Your Username"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Your Password"}),
    )
    keep_logged_in = forms.BooleanField(
        required=False,
        initial=False,
    )

    def clean(self) -> dict[str, Any]:
        cleaned_data = super().clean()

        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        if not username or not password:
            return cleaned_data

        user = authenticate(
            self.request,
            username=username,
            password=password,
        )

        if user is None:
            raise forms.ValidationError("Invalid credentials.")

        if not user.is_active:
            raise forms.ValidationError("Your account is inactive.")

        if not user.is_verified:
            raise forms.ValidationError("Please verify your email first.")

        cleaned_data["user"] = user
        return cleaned_data


# =========================== CHANGE PASSWORD =======================
class ChangePasswordForm(StyledForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Your Old Password"}),
    )
    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Your New Password"}),
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Confirm Your Password"}),
    )

    def clean(self) -> dict[str, Any]:
        cleaned_data = super().clean()

        if not self.request or not hasattr(self.request, "user"):
            raise forms.ValidationError("Request context is required.")

        user = self.request.user

        if not user.is_authenticated:
            raise forms.ValidationError("Authentication required.")

        old_password = cleaned_data.get("old_password")
        new_password = cleaned_data.get("new_password")
        new_password2 = cleaned_data.get("new_password2")

        if not old_password or not new_password or not new_password2:
            return cleaned_data

        if not user.check_password(old_password):
            self.add_error("old_password", "Incorrect old password.")

        if new_password != new_password2:
            self.add_error("new_password2", "Passwords do not match.")

        if old_password == new_password:
            self.add_error("new_password", "New password must be different from old password.")

        try:
            validate_password_strength(new_password)
        except forms.ValidationError as e:
            self.add_error("new_password", e)

        return cleaned_data

    def save(self, commit: bool = True) -> User:
        user = self.request.user
        new_password = self.cleaned_data["new_password"]

        with transaction.atomic():
            user.set_password(new_password)
            user.save(update_fields=["password"])

        update_session_auth_hash(self.request, user)
        return user


# ========================= PASSWORD RESET REQUEST =========================
class PasswordResetForm(StyledForm):
    email = forms.EmailField(
        widget=forms.TextInput(attrs={"placeholder": "Your Email"})
    )

    def clean(self) -> dict[str, Any]:
        cleaned_data = super().clean()
        email = cleaned_data.get("email", "").strip().lower()

        if not email:
            return cleaned_data

        user = User.objects.filter(
            email__iexact=email,
            is_active=True,
            is_verified=True,
        ).first()

        self.user = user

        if user and hasattr(OTPService, 'can_send_otp'):
            if not OTPService.can_send_otp(user.email):
                self.add_error("email", "Please wait before requesting another OTP.")

        return cleaned_data

    def save(self, commit: bool = True) -> User | None:
        user = getattr(self, "user", None)
        if not user:
            return None

        otp = OTPService.generate()
        OTPService.save(user.email, otp)

        email = user.email
        transaction.on_commit(lambda e=email, o=otp: send_password_reset_email.delay(e, o))
        return user


# ========================= PASSWORD RESET CONFIRM =========================
class PasswordResetConfirmForm(StyledForm):
    email = forms.EmailField(
        widget=forms.TextInput(attrs={"placeholder": "Your Email"})
    )
    otp = forms.CharField(
        min_length=6,
        max_length=6,
        widget=forms.TextInput(attrs={
            "placeholder": "Your 6-digit OTP",
            "maxlength": "6"
        })
    )
    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Your New Password"}),
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Confirm Your Password"}),
    )

    def clean(self) -> dict[str, Any]:
        cleaned_data = super().clean()

        email = cleaned_data.get("email", "").strip().lower()
        otp = cleaned_data.get("otp", "").strip()
        password = cleaned_data.get("new_password")
        password2 = cleaned_data.get("new_password2")

        if not email or not otp or not password or not password2:
            return cleaned_data

        if password != password2:
            self.add_error("new_password2", "Passwords do not match.")
        else:
            try:
                validate_password_strength(password)
            except forms.ValidationError as e:
                self.add_error("new_password", e)

        user = User.objects.filter(
            email__iexact=email,
            is_active=True,
            is_verified=True,
        ).first()

        if user is None:
            self.add_error("email", "Invalid email.")
            return cleaned_data

        if not OTPService.verify(user.email, otp):
            self.add_error("otp", "Invalid or expired OTP.")
            return cleaned_data

        self.user = user
        return cleaned_data

    def save(self, commit: bool = True) -> User:
        user = getattr(self, "user", None)
        if not user:
            raise ValueError("Cannot reset password without valid user context.")

        with transaction.atomic():
            user.set_password(self.cleaned_data["new_password"])
            user.save(update_fields=["password"])

        return user


# ===================== RESEND EMAIL ================================
class ResendVerifyEmailForm(StyledForm):
    email = forms.EmailField(
        widget=forms.TextInput(attrs={"placeholder": "Your Email"})
    )

    def clean(self) -> dict[str, Any]:
        cleaned_data = super().clean()
        email = cleaned_data.get("email", "").strip().lower()

        if not email:
            return cleaned_data

        user = User.objects.filter(email__iexact=email).first()

        if user is None:
            self.add_error("email", "User does not exist.")
            return cleaned_data

        if user.is_verified:
            self.add_error("email", "Email is already verified.")
            return cleaned_data

        if hasattr(OTPService, 'can_send_otp') and not OTPService.can_send_otp(user.email):
            self.add_error("email", "Please wait before requesting another OTP.")

        self.user = user
        return cleaned_data

    def save(self, commit: bool = True) -> User:
        user = getattr(self, "user", None)
        if not user:
            raise ValueError("User context missing.")

        otp = OTPService.generate()

        OTPService.save(user.email, otp)
        email = user.email
        transaction.on_commit(lambda e=email, o=otp: send_verification_email.delay(e, o))

        return user


# ===================== PROFILE ================================
class ProfileForm(forms.ModelForm, StyledForm):
    class Meta:
        model = User
        fields = ["username", "email", "phone", "image"]
        widgets = {
            "image": forms.FileInput(attrs={"accept": "image/*"}),
        }

    def clean_username(self) -> str:
        username = self.cleaned_data.get("username", "").strip().lower()
        if User.objects.filter(username__iexact=username).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Username already taken by another user.")
        return username

    def clean_email(self) -> str:
        email = self.cleaned_data.get("email", "").strip().lower()
        if User.objects.filter(email__iexact=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Email already used by another user.")
        return email

    def clean_phone(self) -> str | None:
        phone = self.cleaned_data.get("phone")
        if phone and User.objects.filter(phone=phone).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Phone number already used by another user.")
        return phone