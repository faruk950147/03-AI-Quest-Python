import re
from typing import Any
from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password  # Added missing import
from django.db import transaction

from account.services import TokenService
from account.tasks import (
    send_password_reset_email,
    send_verification_email,
)

User = get_user_model()


# ============================================================
# PASSWORD VALIDATION
# ============================================================
def validate_password_strength(password: str) -> str:
    """
    Validate application password policy.
    """
    if len(password) < 8:
        raise forms.ValidationError("Password must be at least 8 characters.")

    if not re.search(r"[A-Z]", password):
        raise forms.ValidationError("Password must contain an uppercase letter.")

    if not re.search(r"[a-z]", password):
        raise forms.ValidationError("Password must contain a lowercase letter.")

    if not re.search(r"\d", password):
        raise forms.ValidationError("Password must contain a number.")

    return password


# ============================================================
# BASE STYLED FORM
# ============================================================
class StyledForm(forms.Form):
    """
    Base form for consistent Bootstrap styling.
    """
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field.widget, (
                forms.TextInput, forms.PasswordInput, forms.EmailInput, 
                forms.NumberInput, forms.Textarea,
            )):
                field.widget.attrs.setdefault("class", "form-control")


# ============================================================
# SIGNUP FORM
# ============================================================
class SignupForm(StyledForm, forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Your password"}),
        strip=False,
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Your confirm password"}),
        strip=False,
        label="Confirm password",
    )

    class Meta:
        model = User
        fields = ["username", "email", "phone", "password", "password2"]
        widgets = {
            "username": forms.TextInput(attrs={"placeholder": "Your username"}),
            "email": forms.EmailInput(attrs={"placeholder": "Your email"}),
            "phone": forms.TextInput(attrs={"placeholder": "Your phone number"}),
        }

    def clean_email(self) -> str:
        email: str = self.cleaned_data.get("email", "")
        return email.strip().lower()

    def clean(self) -> dict[str, Any]:
        cleaned_data: dict[str, Any] = super().clean()
        password: str | None = cleaned_data.get("password")
        password2: str | None = cleaned_data.get("password2")

        # PASSWORD MATCH
        if password and password2 and password != password2:
            self.add_error("password2", "Passwords do not match.")

        # PASSWORD STRENGTH & DJANGO VALIDATION
        if password:
            try:
                validate_password_strength(password)
            except forms.ValidationError as exc:
                self.add_error("password", exc)

            try:
                validate_password(password)
            except forms.ValidationError as exc:
                self.add_error("password", exc)

        return cleaned_data

    def save(self, commit: bool = True) -> User:
        user: User = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])

        user.is_active = False
        user.is_verified = False

        if not commit:
            return user

        with transaction.atomic():
            user.save()
            token: str | None = TokenService.issue(
                identifier=user.email,
                purpose=TokenService.EMAIL_VERIFICATION,
                timeout=TokenService.email_verification_timeout(),
            )

            if token is None:
                raise RuntimeError("Failed to generate email verification token.")

            transaction.on_commit(
                lambda email=user.email, tok=token: send_verification_email.delay(email, tok)
            )

        return user


# ============================================================
# EMAIL VERIFICATION FORM
# ============================================================
class EmailVerificationForm(StyledForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"placeholder": "Your Email"})
    )
    token = forms.CharField(
        strip=True,
        widget=forms.TextInput(attrs={"placeholder": "Your Token"}),
    )

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.user: User | None = None

    def clean_email(self) -> str:
        email: str = self.cleaned_data["email"]
        return email.strip().lower()

    def clean(self) -> dict[str, Any]:
        cleaned_data: dict[str, Any] = super().clean()
        email: str | None = cleaned_data.get("email")
        token: str | None = cleaned_data.get("token")

        if not email or not token:
            return cleaned_data

        user: User | None = User.objects.filter(email=email).first()

        if not user:
            self.add_error("email", "Invalid verification request.")
            return cleaned_data

        if user.is_verified:
            self.add_error("email", "Account already verified.")
            return cleaned_data

        is_valid: bool = TokenService.verify(
            identifier=email,
            purpose=TokenService.EMAIL_VERIFICATION,
            token=token,
        )

        if not is_valid:
            self.add_error("token", "Invalid or expired verification token.")
            return cleaned_data

        self.user = user
        return cleaned_data

    def save(self, commit: bool = True) -> User:
        if not self.user:
            raise ValueError("Cannot call save() on an invalidated or failed form.")

        self.user.is_verified = True
        self.user.is_active = True

        if not commit:
            return self.user

        with transaction.atomic():
            self.user.save(
                update_fields=["is_verified", "is_active", "updated_at"]
            )

        return self.user


# ============================================================
# LOGIN FORM
# ============================================================
class LoginForm(StyledForm):
    username = forms.CharField(
        max_length=150,
        strip=True,
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Your Username"}),
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Your Password"}),
        strip=False,
    )

    keep_logged_in = forms.BooleanField(
        required=False,
        initial=False,
    )

    def __init__(self, *args: Any, request: Any = None, **kwargs: Any) -> None:
        self.request = request
        self.user: Any | None = None
        super().__init__(*args, **kwargs)

    def clean(self) -> dict[str, Any]:
        cleaned_data: dict[str, Any] = super().clean()

        username: str | None = cleaned_data.get("username")
        password: str | None = cleaned_data.get("password")

        if not username or not password:
            return cleaned_data

        user = authenticate(
            request=self.request,
            username=username,
            password=password,
        )

        if user is None:
            raise forms.ValidationError("Invalid credentials.")

        if not user.is_active:
            raise forms.ValidationError("Your account is inactive.")

        if not user.is_verified:
            raise forms.ValidationError("Please verify your email first.")

        self.user = user
        cleaned_data["user"] = user

        return cleaned_data


# ============================================================
# CHANGE PASSWORD FORM
# ============================================================
class ChangePasswordForm(StyledForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"autocomplete": "current-password"}
        ),
        strip=False,
    )
    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        strip=False,
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        strip=False,
        label="Confirm new password",
    )

    def __init__(self, user: User, *args: Any, **kwargs: Any) -> None:
        self.user: User = user
        super().__init__(*args, **kwargs)

    def clean(self) -> dict[str, Any]:
        cleaned_data: dict[str, Any] = super().clean()
        old_password: str | None = cleaned_data.get("old_password")
        new_password: str | None = cleaned_data.get("new_password")
        new_password2: str | None = cleaned_data.get("new_password2")

        if not old_password or not self.user.check_password(old_password):
            self.add_error("old_password", "Old password is incorrect.")

        if new_password and new_password2 and new_password != new_password2:
            self.add_error("new_password2", "Passwords do not match.")

        if old_password and new_password and old_password == new_password:
            self.add_error(
                "new_password",
                "New password must be different from old password.",
            )

        if new_password:
            try:
                validate_password_strength(new_password)
            except forms.ValidationError as exc:
                self.add_error("new_password", exc)

            try:
                validate_password(new_password, user=self.user)
            except forms.ValidationError as exc:
                self.add_error("new_password", exc)

        return cleaned_data

    def save(self, commit: bool = True) -> User:
        self.user.set_password(self.cleaned_data["new_password"])

        if not commit:
            return self.user

        with transaction.atomic():
            self.user.save(update_fields=["password", "updated_at"])

        return self.user


# ============================================================
# PASSWORD RESET REQUEST FORM
# ============================================================
class PasswordResetRequestForm(StyledForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"placeholder": "Your Email"})
    )

    def clean_email(self) -> str:
        email: str = self.cleaned_data["email"]
        return email.strip().lower()

    def save(self) -> dict[str, str]:
        email: str = self.cleaned_data["email"]

        response: dict[str, str] = {
            "message": (
                "If the email exists, "
                "a password reset link "
                "has been sent."
            )
        }

        user: User | None = User.objects.filter(
            email=email,
            is_verified=True,
            is_active=True,
        ).first()

        if not user:
            return response

        with transaction.atomic():
            token: str | None = TokenService.issue(
                identifier=email,
                purpose=TokenService.PASSWORD_RESET,
                timeout=TokenService.password_reset_timeout(),
            )

            if token is None:
                raise RuntimeError("Failed to generate password reset token.")

            transaction.on_commit(
                lambda user_email=user.email, tok=token: (
                    send_password_reset_email.delay(user_email, tok)
                )
            )

        return response


# ============================================================
# PASSWORD RESET CONFIRM FORM
# ============================================================
class PasswordResetConfirmForm(StyledForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"placeholder": "Your Email"})
    )
    token = forms.CharField(
        strip=True,
        widget=forms.TextInput(attrs={"placeholder": "Reset Token"}),
    )
    new_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"autocomplete": "new-password", "placeholder": "New Password"}
        ),
        strip=False,
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"autocomplete": "new-password", "placeholder": "Confirm New Password"}
        ),
        strip=False,
        label="Confirm new password",
    )

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.user: User | None = None

    def clean_email(self) -> str:
        email: str = self.cleaned_data["email"]
        return email.strip().lower()

    def clean(self) -> dict[str, Any]:
        cleaned_data: dict[str, Any] = super().clean()
        email: str | None = cleaned_data.get("email")
        token: str | None = cleaned_data.get("token")
        new_password: str | None = cleaned_data.get("new_password")
        new_password2: str | None = cleaned_data.get("new_password2")

        if new_password and new_password2 and new_password != new_password2:
            self.add_error("new_password2", "Passwords do not match.")

        if new_password:
            try:
                validate_password_strength(new_password)
            except forms.ValidationError as exc:
                self.add_error("new_password", exc)

        if not email or not token or not new_password or not new_password2 or self.errors:
            return cleaned_data

        user: User | None = User.objects.filter(email=email, is_verified=True, is_active=True).first()

        if not user:
            self.add_error(None, "Invalid password reset request.")
            return cleaned_data

        try:
            validate_password(new_password, user=user)
        except forms.ValidationError as exc:
            self.add_error("new_password", exc)
            return cleaned_data

        is_valid: bool = TokenService.verify(
            identifier=email,
            purpose=TokenService.PASSWORD_RESET,
            token=token,
        )

        if not is_valid:
            self.add_error("token", "Invalid or expired reset token.")
            return cleaned_data

        self.user = user
        return cleaned_data

    def save(self, commit: bool = True) -> User:
        if not self.user:
            raise ValueError("Cannot call save() on an unvalidated or failed form.")

        self.user.set_password(self.cleaned_data["new_password"])

        if not commit:
            return self.user

        with transaction.atomic():
            self.user.save(update_fields=["password", "updated_at"])

        return self.user


# ============================================================
# RESEND EMAIL VERIFICATION FORM
# ============================================================
class ResendVerificationEmailForm(StyledForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"placeholder": "Your Email"})
    )

    def clean_email(self) -> str:
        email: str = self.cleaned_data["email"]
        return email.strip().lower()

    def save(self) -> dict[str, str]:
        email: str = self.cleaned_data["email"]

        response: dict[str, str] = {
            "message": (
                "If the account exists and requires verification, "
                "a verification email has been sent."
            )
        }

        user: User | None = User.objects.filter(
            email=email,
            is_verified=False,
        ).first()

        if not user:
            return response

        with transaction.atomic():
            token: str | None = TokenService.issue(
                identifier=email,
                purpose=TokenService.EMAIL_VERIFICATION,
                timeout=TokenService.email_verification_timeout(),
            )

            if token is None:
                raise RuntimeError(
                    "Failed to generate email verification token."
                )

            transaction.on_commit(
                lambda user_email=user.email, tok=token: (
                    send_verification_email.delay(user_email, tok)
                )
            )

        return response