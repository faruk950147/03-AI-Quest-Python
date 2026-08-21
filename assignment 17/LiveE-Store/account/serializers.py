import re
from typing import Any

from django.contrib.auth import (
    authenticate,
    get_user_model,
    update_session_auth_hash,
)
from django.db import transaction
from rest_framework import serializers
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from account.services import TokenService
from account.tasks import (
    send_password_reset_email,
    send_verification_email,
)

User = get_user_model()


# ============================================================
# PASSWORD VALIDATION
# ============================================================

def validate_password(password: str) -> str:
    """
    Validate application password policy.
    """
    if len(password) < 8:
        raise serializers.ValidationError("Password must be at least 8 characters.")

    if not re.search(r"[A-Z]", password):
        raise serializers.ValidationError("Password must contain an uppercase letter.")

    if not re.search(r"[a-z]", password):
        raise serializers.ValidationError("Password must contain a lowercase letter.")

    if not re.search(r"\d", password):
        raise serializers.ValidationError("Password must contain a number.")

    return password


# ============================================================
# SIGNUP
# ============================================================

class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, trim_whitespace=False)
    password2 = serializers.CharField(write_only=True, trim_whitespace=False)

    class Meta:
        model = User
        fields = ["username", "email", "phone", "password", "password2"]

    # ========================================================
    # VALIDATE
    # ========================================================

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        email = attrs.get("email")
        if email:
            attrs["email"] = email.strip().lower()

        password = attrs["password"]
        password2 = attrs["password2"]

        if password != password2:
            raise serializers.ValidationError({"password2": "Password mismatching."})

        validate_password(password)
        return attrs

    # ========================================================
    # CREATE
    # ========================================================

    def create(self, validated_data: dict[str, Any]) -> User:
        password = validated_data.pop("password")
        validated_data.pop("password2")

        with transaction.atomic():
            user = User.objects.create_user(
                password=password,
                is_active=False,
                is_verified=False,
                **validated_data,
            )

            token = TokenService.issue(
                identifier=user.email,
                purpose=TokenService.EMAIL_VERIFICATION,
                timeout=TokenService.email_verification_timeout(),
            )

            if token is None:
                raise serializers.ValidationError({"email": "Unable to create verification token."})

            transaction.on_commit(
                lambda user=user.email, tok=token: send_verification_email(user, tok)
            )

        return user


# ============================================================
# EMAIL VERIFICATION
# ============================================================

class VerifyEmailSerializer(serializers.Serializer):
    token = serializers.CharField(trim_whitespace=True)
    email = serializers.EmailField()

    # ========================================================
    # VALIDATE
    # ========================================================

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        email = attrs["email"].strip().lower()
        token = attrs["token"].strip()

        user = User.objects.filter(email=email).first()

        if not user:
            raise serializers.ValidationError("Invalid verification request.")

        if user.is_verified:
            raise serializers.ValidationError("Account already verified.")

        is_valid = TokenService.verify(
            identifier=email,
            purpose=TokenService.EMAIL_VERIFICATION,
            token=token,
        )

        if not is_valid:
            raise serializers.ValidationError("Invalid or expired verification token.")

        attrs["email"] = email
        attrs["token"] = token
        attrs["user"] = user

        return attrs

    # ========================================================
    # SAVE
    # ========================================================

    def save(self) -> User:
        user = self.validated_data["user"]

        user.is_verified = True
        user.is_active = True

        user.save(
            update_fields=[
                "is_verified",
                "is_active",
                "updated_at",
            ]
        )

        return user


# ============================================================
# LOGIN
# ============================================================

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, trim_whitespace=True)
    password = serializers.CharField(
        write_only=True,
        trim_whitespace=False,
        style={"input_type": "password"},
    )
    keep_logged_in = serializers.BooleanField(
        required=False,
        default=False,
    )

    # ========================================================
    # VALIDATE
    # ========================================================

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        username = attrs["username"].strip().lower()
        password = attrs["password"]

        user = authenticate(
            self.context.get("request"),
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
                "phone": getattr(user, "phone", None),
            },
            "tokens": {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            },
        }


# ============================================================
# LOGOUT
# ============================================================

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField(trim_whitespace=True)

    # ========================================================
    # VALIDATE
    # ========================================================

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        try:
            token = RefreshToken(attrs["refresh"].strip())
        except TokenError as exc:
            raise serializers.ValidationError("Invalid or expired refresh token.") from exc

        attrs["token_obj"] = token
        return attrs

    # ========================================================
    # SAVE
    # ========================================================

    def save(self) -> dict[str, str]:
        token: RefreshToken = self.validated_data["token_obj"]
        try:
            token.blacklist()
        except TokenError as exc:
            raise serializers.ValidationError("Invalid or expired refresh token.") from exc

        return {"message": "Logout successful."}


# ============================================================
# CHANGE PASSWORD
# ============================================================

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True, trim_whitespace=False)
    new_password = serializers.CharField(write_only=True, trim_whitespace=False)
    new_password2 = serializers.CharField(write_only=True, trim_whitespace=False)

    # ========================================================
    # VALIDATE
    # ========================================================

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        user = self.context["request"].user

        if not user.check_password(attrs["old_password"]):
            raise serializers.ValidationError({"old_password": "Wrong old password."})

        if attrs["new_password"] != attrs["new_password2"]:
            raise serializers.ValidationError({"new_password2": "Password mismatching."})

        if attrs["old_password"] == attrs["new_password"]:
            raise serializers.ValidationError(
                {"new_password": "New password must be different from old password."}
            )

        validate_password(attrs["new_password"])

        return attrs

    # ========================================================
    # SAVE
    # ========================================================

    def save(self) -> User:
        user = self.context["request"].user

        user.set_password(self.validated_data["new_password"])
        user.save(
            update_fields=[
                "password",
                "updated_at",
            ]
        )

        update_session_auth_hash(self.context["request"], user)

        # Optional: Revoke existing user tokens
        # TokenService.revoke_user_tokens(user)

        return user


# ============================================================
# PASSWORD RESET REQUEST
# ============================================================

class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    # ========================================================
    # VALIDATE
    # ========================================================

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        attrs["email"] = attrs["email"].strip().lower()
        return attrs

    # ========================================================
    # SAVE
    # ========================================================

    def save(self) -> dict[str, str]:
        email = self.validated_data["email"]
        generic_message = "If the email exists, a password reset link has been sent."

        user = User.objects.filter(
            email=email,
            is_verified=True,
            is_active=True,
        ).first()

        if not user:
            return {"message": generic_message}

        with transaction.atomic():
            token = TokenService.issue(
                identifier=email,
                purpose=TokenService.PASSWORD_RESET,
                timeout=TokenService.password_reset_timeout(),
            )

            if token is not None:
                transaction.on_commit(
                    lambda user=user.email, tok=token: send_password_reset_email(user, tok)
                )

        return {"message": generic_message}


# ============================================================
# PASSWORD RESET CONFIRM
# ============================================================

class PasswordResetConfirmSerializer(serializers.Serializer):
    email = serializers.EmailField()
    token = serializers.CharField(trim_whitespace=True)
    new_password = serializers.CharField(write_only=True, trim_whitespace=False)
    new_password2 = serializers.CharField(write_only=True, trim_whitespace=False)

    # ========================================================
    # VALIDATE
    # ========================================================

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        email = attrs["email"].strip().lower()
        token = attrs["token"].strip()

        if attrs["new_password"] != attrs["new_password2"]:
            raise serializers.ValidationError({"new_password2": "Password mismatching."})

        validate_password(attrs["new_password"])

        user = User.objects.filter(
            email=email,
            is_verified=True,
            is_active=True,
        ).first()

        if not user:
            raise serializers.ValidationError("Invalid password reset request.")

        is_valid = TokenService.verify(
            identifier=email,
            purpose=TokenService.PASSWORD_RESET,
            token=token,
        )

        if not is_valid:
            raise serializers.ValidationError("Invalid or expired reset token.")

        attrs["email"] = email
        attrs["token"] = token
        attrs["user"] = user

        return attrs

    # ========================================================
    # SAVE
    # ========================================================

    def save(self) -> dict[str, str]:
        user = self.validated_data["user"]

        user.set_password(self.validated_data["new_password"])
        user.save(update_fields=["password", "updated_at"])

        # Optional: Invalidate existing refresh tokens post password reset
        # TokenService.revoke_user_tokens(user)

        return {"message": "Password reset successful."}


# ============================================================
# RESEND EMAIL VERIFICATION
# ============================================================

class ResendVerificationEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()

    # ========================================================
    # VALIDATE
    # ========================================================

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        attrs["email"] = attrs["email"].strip().lower()
        return attrs

    # ========================================================
    # SAVE
    # ========================================================

    def save(self) -> dict[str, str]:
        email = self.validated_data["email"]
        generic_message = "If the account exists, a verification email has been sent."

        user = User.objects.filter(
            email=email,
            is_verified=False,
        ).first()

        if not user:
            return {"message": generic_message}

        with transaction.atomic():
            token = TokenService.issue(
                identifier=email,
                purpose=TokenService.EMAIL_VERIFICATION,
                timeout=TokenService.email_verification_timeout(),
            )

            if token is not None:
                transaction.on_commit(
                    lambda user=user.email, tok=token: send_verification_email(user, tok)
                )

        return {"message": generic_message}