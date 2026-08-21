import re

from django.db import transaction
from django.db.models import Q
from typing import Any
from typing import Optional
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, update_session_auth_hash

from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from account.services import OTPService
from account.tasks import send_verification_email, send_password_reset_email

User = get_user_model()


# ========================= PASSWORD VALIDATION =========================
def validate_password(password):
    if len(password) < 8:
        raise serializers.ValidationError("Password must be at least 8 characters.")

    if not re.search(r"[A-Z]", password):
        raise serializers.ValidationError("Password must contain at least one uppercase letter.")

    if not re.search(r"[a-z]", password):
        raise serializers.ValidationError("Password must contain at least one lowercase letter.")

    if not re.search(r"\d", password):
        raise serializers.ValidationError("Password must contain at least one number.")

    return password

# ========================= SIGNUP =========================
class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        trim_whitespace=True,
        style={"input_type": "password"},
    )
    password2 = serializers.CharField(
        write_only=True,
        trim_whitespace=True,
        style={"input_type": "password"},
    )

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "phone",
            "password",
            "password2",
        )

    def validate_username(self, value: str) -> str:
        value = value.strip().lower()

        if User.objects.filter(username__iexact=value).exists():
            raise serializers.ValidationError("Username already exists.")

        return value

    def validate_email(self, value: str) -> str:
        value = value.strip().lower()

        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("Email already exists.")

        return value

    def validate_phone(self, value: str) -> str:
        if User.objects.filter(phone=value).exists():
            raise serializers.ValidationError("Phone already exists.")

        return value

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        password = attrs.get("password")
        password2 = attrs.pop("password2")

        if password != password2:
            raise serializers.ValidationError({"password2": "Passwords do not match."})

        validate_password(password)

        return attrs

    def create(self, validated_data: dict[str, Any]) -> User:
        password = validated_data.pop("password")
        email = validated_data["email"]

        otp = OTPService.generate()

        if not OTPService.save(email, otp):
            raise serializers.ValidationError({"email": "Unable to send OTP. Please try again later."})

        with transaction.atomic():
            user = User.objects.create_user(
                password=password,
                is_active=False,
                is_verified=False,
                **validated_data,
            )

            transaction.on_commit(lambda: send_verification_email.delay(email, otp))

        return user
    
# ========================= EMAIL VERIFICATION =========================
class VerifyEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(
        min_length=6,
        max_length=6,
        trim_whitespace=True,
    )

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        email = attrs["email"].strip().lower()
        otp = attrs["otp"].strip()

        user = User.objects.filter(email__iexact=email).first()

        if user is None:
            raise serializers.ValidationError({"email": "User does not exist."})

        if user.is_verified:
            raise serializers.ValidationError({"email": "Email is already verified."})

        if not OTPService.verify(user.email, otp):
            raise serializers.ValidationError({"otp": "Invalid or expired OTP."})

        attrs["user"] = user
        return attrs

    def save(self, **kwargs) -> User:
        user = self.validated_data["user"]

        with transaction.atomic():
            user.is_verified = True
            user.is_active = True
            user.save(update_fields=[
                "is_verified",
                "is_active",
            ])

        return user


# ========================= LOGIN =========================
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=150,
        trim_whitespace=True,
    )

    password = serializers.CharField(
        write_only=True,
        trim_whitespace=True,
        style={"input_type": "password"},
    )

    keep_logged_in = serializers.BooleanField(
        required=False,
        default=False,
    )

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        username = attrs["username"].strip().lower()
        password = attrs["password"]


        user = authenticate(
            self.request if hasattr(self, "request") else None,
            username=username,
            password=password,
        )

        if user is None:
            raise serializers.ValidationError({"detail": "Invalid username or email or phone or password."})

        if not user.is_active:
            raise serializers.ValidationError({"detail": "Your account is inactive."})

        if not user.is_verified:
            raise serializers.ValidationError({"detail": "Please verify your email first."})

        refresh = RefreshToken.for_user(user)

        return {
            "user": {
                "id": user.pk,
                "username": user.username,
                "email": user.email,
                "phone": user.phone,
            },
            "tokens": {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            },
        }


# ====================== LOGOUT ================================
class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField(
        write_only=True,
        trim_whitespace=True,
    )

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        self.refresh_token = attrs["refresh"].strip()

        if not self.refresh_token:
            raise serializers.ValidationError({"refresh": "Refresh token is required."})

        return attrs

    def save(self, **kwargs) -> None:
        try:
            token = RefreshToken(self.refresh_token)
            token.blacklist()
        except TokenError:
            raise serializers.ValidationError({"refresh": "Invalid or expired refresh token."})


# ========================= CHANGE PASSWORD =========================
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(
        write_only=True,
        trim_whitespace=True,
        style={"input_type": "password"},
    )
    new_password = serializers.CharField(
        write_only=True,
        trim_whitespace=True,
        style={"input_type": "password"},
    )
    new_password2 = serializers.CharField(
        write_only=True,
        trim_whitespace=True,
        style={"input_type": "password"},
    )

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        user = self.context["request"].user

        if not user.check_password(attrs["old_password"]):
            raise serializers.ValidationError({"old_password": "Incorrect old password."})

        if attrs["new_password"] != attrs["new_password2"]:
            raise serializers.ValidationError({"new_password2": "Passwords do not match."})

        if attrs["old_password"] == attrs["new_password"]:
            raise serializers.ValidationError( {"new_password": "New password must be different from the old password."})

        validate_password(attrs["new_password"])

        return attrs

    def save(self) -> User:
        user = self.context["request"].user

        with transaction.atomic():
            user.set_password(self.validated_data["new_password"])
            user.save(update_fields=["password"])

        update_session_auth_hash(self.context["request"], user)

        return user


# ========================= PASSWORD RESET REQUEST =========================
class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        email = attrs["email"].strip().lower()

        self.user = User.objects.filter(
            email__iexact=email,
            is_active=True,
            is_verified=True,
        ).first()

        attrs["email"] = email
        return attrs

    def save(self) -> User | None:
        if not self.user:
            return None

        otp = OTPService.generate()

        if not OTPService.save(self.user.email, otp):
            raise serializers.ValidationError({"email": "Please wait before requesting another OTP."})

        transaction.on_commit(lambda: send_password_reset_email.delay(self.user.email, otp))

        return self.user


# ========================= PASSWORD RESET CONFIRM =========================
class PasswordResetConfirmSerializer(serializers.Serializer):
    email = serializers.EmailField()

    otp = serializers.CharField(
        min_length=6,
        max_length=6,
        trim_whitespace=True,
    )

    new_password = serializers.CharField(
        write_only=True,
        trim_whitespace=True,
        style={"input_type": "password"},
    )

    new_password2 = serializers.CharField(
        write_only=True,
        trim_whitespace=True,
        style={"input_type": "password"},
    )

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        email = attrs["email"].strip().lower()
        otp = attrs["otp"].strip()

        if attrs["new_password"] != attrs["new_password2"]:
            raise serializers.ValidationError({"new_password2": "Passwords do not match."})

        validate_password(attrs["new_password"])

        user = User.objects.filter(
            email__iexact=email,
            is_active=True,
            is_verified=True,
        ).first()

        if user is None:
            raise serializers.ValidationError({"email": "Invalid email."})

        if not OTPService.verify(user.email, otp):
            raise serializers.ValidationError({"otp": "Invalid or expired OTP."})

        attrs["user"] = user

        return attrs

    def save(self) -> User:
        user = self.validated_data["user"]

        with transaction.atomic():
            user.set_password(self.validated_data["new_password"])

            user.save(update_fields=["password"])

        return user


# ===================== RESEND EMAIL ================================
class ResendVerificationEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        email = attrs["email"].strip().lower()

        user = User.objects.filter(email__iexact=email).first()

        if user is None:
            raise serializers.ValidationError({"email": "User does not exist."})

        if user.is_verified:
            raise serializers.ValidationError({"email": "Email is already verified."})

        attrs["user"] = user
        attrs["email"] = email

        return attrs

    def save(self) -> User:
        user = self.validated_data["user"]

        otp = OTPService.generate()

        if not OTPService.save(user.email, otp):
            raise serializers.ValidationError({"email": "Please wait before requesting another OTP."})

        transaction.on_commit(lambda: send_verification_email.delay(user.email, otp))

        return user