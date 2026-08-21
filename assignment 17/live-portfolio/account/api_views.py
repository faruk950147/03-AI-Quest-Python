from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
)

from account.serializers import (
    SignupSerializer,
    VerifyEmailSerializer,
    LoginSerializer,
    LogoutSerializer,
    ChangePasswordSerializer,
    PasswordResetSerializer,
    PasswordResetConfirmSerializer,
    ResendVerificationEmailSerializer,
)


# ========================= RESPONSE HELPERS =========================

def success(message, data=None, code=200):
    return Response(
        {
            "success": True,
            "message": message,
            "data": data,
        },
        status=code,
    )


def error(message, code=400):
    return Response(
        {
            "success": False,
            "message": message,
        },
        status=code,
    )


# ========================= ROOT API =========================

class RootAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):

        return Response(
            {
                "message": "Account API is running.",
                "endpoints": {
                    "signup": "http://127.0.0.1:8000/api/account/signup/",
                    "verify_email": "http://127.0.0.1:8000/api/account/verify/email/",
                    "login": "http://127.0.0.1:8000/api/account/login/",
                    "logout": "http://127.0.0.1:8000/api/account/logout",
                    "change_password": "http://127.0.0.1:8000/api/account/change/password/",
                    "password_reset": "http://127.0.0.1:8000/password/reset/",
                    "password_reset_confirm": "http://127.0.0.1:8000/password/reset/confirm/",
                    "resend_verify_email": "http://127.0.0.1:8000/resend/verify/email/",
                },
            }
        )


# ========================= SIGNUP =========================
class SignupViewAPI(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignupSerializer( data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return success(
            "Signup successful. Verify your email.", {
                "user_id": user.id,
                "email": user.email,
            }, status.HTTP_201_CREATED)


# ========================= VERIFY EMAIL =========================
class VerifyEmailViewAPI(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = VerifyEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return success(
            "Email verified successfully.",{
                "user_id": user.id,
                "email": user.email,
            })


# ========================= LOGIN =========================
class LoginViewAPI(APIView):
    permission_classes = [AllowAny]

    def post(self, request):

        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return success("Login successful.", serializer.validated_data)


# ========================= LOGOUT =========================
class LogoutViewAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return success("Logout successful.")


# ========================= CHANGE PASSWORD =========================
class ChangePasswordViewAPI(APIView):

    def post(self, request):

        serializer = ChangePasswordSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return success("Password changed successfully.")


# ========================= PASSWORD RESET REQUEST =========================
class PasswordResetViewAPI(APIView):
    permission_classes = [AllowAny]

    def post(self, request):

        serializer = PasswordResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return success("OTP has been sent.", {"email": user.email if user else None})


# ========================= PASSWORD RESET CONFIRM =========================
class PasswordResetConfirmViewAPI(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return success("Password reset successful.", {"user_id": user.id, "email": user.email})


# ========================= RESEND VERIFICATION EMAIL =========================
class ResendVerifyEmailViewAPI(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ResendVerificationEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return success("Verification OTP has been resent.", { "email": user.email})