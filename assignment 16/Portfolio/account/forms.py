import re
from typing import Any

from django import forms
from django.db import transaction
from django.db.models import Q
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
        raise forms.ValidationError(
            "Password must contain at least one uppercase letter."
        )

    if not re.search(r"[a-z]", password):
        raise forms.ValidationError(
            "Password must contain at least one lowercase letter."
        )

    if not re.search(r"\d", password):
        raise forms.ValidationError(
            "Password must contain at least one number."
        )

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


# ========================= SIGNUP FORM =========================
class SignupForm(StyledForm, forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Your Password"}),
        strip=True
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Confirm Your Password"}),
        strip=True
    )
    class Meta:
        model = User
        fields = ["username", "email", "phone", "password", "password2"]
        
        widgets = {
            "username": forms.TextInput(attrs={"placeholder": "Your username"}),
            "email": forms.EmailInput(attrs={"placeholder": "Your email"}),
            "phone": forms.TextInput(attrs={"placeholder": "Your phone number"}),
        }

    def clean_username(self) -> str:
        username = self.cleaned_data["username"].strip().lower()

        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError("Username already exists.")

        return username

    def clean_email(self) -> str:
        email = self.cleaned_data["email"].strip().lower()

        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Email already exists.")

        return email

    def clean_phone(self) -> str:
        phone = self.cleaned_data.get("phone")

        if User.objects.filter(phone=phone).exists():
            raise forms.ValidationError("Phone number already exists.")

        return phone

    def clean(self) -> dict[str, Any]:
        cleaned_data = super().clean()

        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")

        if password and password2:
            if password != password2:
                raise forms.ValidationError("Passwords do not match.")

            validate_password_strength(password)

        return cleaned_data
    '''
    def create(self) -> User:
        with transaction.atomic():
            user = User.objects.create_user(
                username=self.cleaned_data["username"],
                email=self.cleaned_data["email"],
                phone=self.cleaned_data["phone"],
                password=self.cleaned_data["password"],
                is_active=False,
                is_verified=False,
            )

            otp = OTPService.generate()
            OTPService.save(user.email, otp)

            transaction.on_commit(
                lambda: send_verification_email(user.email, otp)
            )

        return user
    '''
    
    def save(self, commit: bool = True) -> User:
        user = super().save(commit=False)

        user.set_password(self.cleaned_data["password"])
        user.is_active = False
        user.is_verified = False

        if commit:
            with transaction.atomic():
                user.save()

                otp = OTPService.generate()
                OTPService.save(user.email, otp)

                transaction.on_commit(lambda: send_verification_email(user.email, otp))

        return user


# ========================= VERIFY EMAIL =======================
class VerifyEmailForm(StyledForm):
    email = forms.EmailField(
        widget=forms.TextInput(attrs={
            "placeholder": "Your Email"
        }),
    )

    otp = forms.CharField(
        min_length=6,
        max_length=6,
        strip=True,
        widget=forms.TextInput(attrs={
            "placeholder": "Your 6-digit OTP",
            "maxlength": "6"
        })
    )
    
    def clean(self) -> dict[str, Any]:
        cleaned_data = super().clean()

        email = cleaned_data.get("email", "").strip().lower()
        otp = cleaned_data.get("otp", "").strip()

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

        cleaned_data["user"] = user
        return cleaned_data

    def save(self, commit: bool = True) -> User:
        user = self.cleaned_data["user"]

        with transaction.atomic():
            user.is_verified = True
            user.is_active = True
            user.save(update_fields=[
                "is_verified",
                "is_active",
            ])

        return user 


# ========================= LOGIN FORM =========================
class LoginForm(StyledForm):
    username = forms.CharField(
        max_length=150,
        strip=True,
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Your Username"})
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Your Password"}),
        strip=True
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
            self.request if hasattr(self, "request") else None,
            username=username,
            password=password,
        )

        if user is None:
            raise forms.ValidationError("Invalid username or email or phone or password.")

        if not user.is_active:
            raise forms.ValidationError("Your account is inactive.")

        if not user.is_verified:
            raise forms.ValidationError("Please verify your email first.")

        # Store authenticated user
        cleaned_data["user"] = user

        return cleaned_data


# =========================== CHANGE PASSWORD =======================
class ChangePasswordForm(StyledForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Your Old Password"}),
        strip=True,
    )

    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Your New Password"}),
        strip=True,
    )

    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Confirm Your Password"}),
        strip=True,
    )

    def clean(self) -> dict[str, Any]:
        cleaned_data = super().clean()

        old_password = cleaned_data.get("old_password")
        new_password = cleaned_data.get("new_password")
        new_password2 = cleaned_data.get("new_password2")

        if not self.request:
            raise forms.ValidationError("Request context is required.")

        user = self.request.user

        if not user.is_authenticated:
            raise forms.ValidationError("Authentication required.")

        # Check old password
        if not user.check_password(old_password):
            raise forms.ValidationError({"old_password": "Incorrect old password."})

        # Match new passwords
        if new_password != new_password2:
            raise forms.ValidationError({"new_password2": "Passwords do not match."})

        # Same password check
        if old_password == new_password:
            raise forms.ValidationError({"new_password": "New password must be different from old password."})

        # Password strength
        validate_password_strength(new_password)

        return cleaned_data

    def save(self, commit: bool = True) -> User:
        user = self.request.user

        with transaction.atomic():
            user.set_password(self.validated_data["new_password"])
            user.save(update_fields=["password"])

        update_session_auth_hash(self.context["request"], user)

        return user


# ========================= PASSWORD RESET REQUEST =========================
class PasswordResetForm(StyledForm):
    email = forms.EmailField(
        widget=forms.TextInput(attrs={"placeholder": "Your Email"})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()

        self.user = User.objects.filter(
            email__iexact=email,
            is_active=True,
            is_verified=True,
        ).first()

        return email

    def save(self, commit: bool = True) -> User:
        if not self.user:
            return None

        otp = OTPService.generate()

        if not OTPService.save(self.user.email, otp):
            raise forms.ValidationError({"email": "Please wait before requesting another OTP."})

        transaction.on_commit(lambda: send_password_reset_email(self.user.email, otp))

        return self.user


# ========================= PASSWORD RESET CONFIRM =========================
class PasswordResetConfirmForm(StyledForm):
    email = forms.EmailField(
        widget=forms.TextInput(attrs={
            "placeholder": "Your Email"
        })
    )

    otp = forms.CharField(
        min_length=6,
        max_length=6,
        strip=True,
        widget=forms.TextInput(attrs={
            "placeholder": "Your 6-digit OTP",
            "maxlength": "6"
        })
    )
   
    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Your New Password"}),
        strip=True,
    )

    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Confirm Your Password"}),
        strip=True,
    )

    def clean(self) -> dict[str, Any]:
        cleaned_data = super().clean()

        email = cleaned_data.get("email", "").strip().lower()
        otp = cleaned_data.get("otp", "").strip()
        password = cleaned_data.get("new_password")
        password2 = cleaned_data.get("new_password2")

        # Password match check
        if password and password2:
            if password != password2:
                raise forms.ValidationError({"new_password2": "Passwords do not match."})

        # Password validation
        validate_password_strength(password)

        # User check
        user = User.objects.filter(
            email__iexact=email,
            is_active=True,
            is_verified=True,
        ).first()

        if user is None:
            raise forms.ValidationError({"email": "Invalid email."})

        # OTP verify
        if not OTPService.verify(user.email, otp):
            raise forms.ValidationError({"otp": "Invalid or expired OTP."})

        cleaned_data["user"] = user

        return cleaned_data

    def save(self, commit: bool = True) -> User:
        user = self.cleaned_data["user"]

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

        user = User.objects.filter(
            email__iexact=email
        ).first()

        if user is None:
            raise forms.ValidationError({"email": "User does not exist."})

        if user.is_verified:
            raise forms.ValidationError({"email": "Email is already verified."})

        cleaned_data["user"] = user
        cleaned_data["email"] = email

        return cleaned_data

    def save(self, commit: bool = True) -> User:
        user = self.cleaned_data["user"]

        otp = OTPService.generate()

        if not OTPService.save(user.email, otp):
            raise forms.ValidationError({"email": "Please wait before requesting another OTP."})

        transaction.on_commit(lambda: send_verification_email(user.email, otp))

        return user
    

# ===================== PROFILE ================================
class ProfileForm(StyledForm, forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email", "phone", "image"]

        widgets = {
            "image": forms.FileInput(attrs={
                "accept": "image/*",
            }),
        }



    
    
    
    
    
    
    
    