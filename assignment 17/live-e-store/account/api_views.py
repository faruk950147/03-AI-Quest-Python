from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.reverse import reverse

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


# =========================================================
# BASE RESPONSE HELPER
# =========================================================
def success(message, data=None, code=200):
    return Response({
        "success": True,
        "message": message,
        "data": data
    }, status=code)


def error(message, code=400):
    return Response({
        "success": False,
        "message": message
    }, status=code)

# ============================ API ROOT ============================
class APIRoot(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({
            "signup": "/api/account/signup/",
            "verify_email": "/api/account/verify/email/",
            "login": "/api/account/login/",
            "logout": "/api/account/logout/",
            "change_password": "/api/account/change/password/",
            "password_reset": "/api/account/password/reset/",
            "password_reset_confirm": "/api/account/password/reset/confirm/",
            "resend_email": "/api/account/resend/email/",
        })

# ============================ SIGNUP ============================
class SignupViewAPI(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return success(
            "Signup successful. Verify your email.",
            {"user_id": user.id},
            status.HTTP_201_CREATED
        )

# ============================ VERIFY EMAIL ============================
class VerifyEmailViewAPI(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = VerifyEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return success("Email verified successfully")

# =========================== LOGIN ============================
class LoginViewAPI(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return success(
            "Login successful",
            serializer.validated_data
        )

# ========================== LOGOUT ============================
class LogoutViewAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return success("Logged out successfully")

# ========================== CHANGE PASSWORD ============================
class ChangePasswordViewAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(
            data=request.data,
            context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return success("Password changed successfully")

# ========================== PASSWORD RESET ============================
class PasswordResetViewAPI(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return success("If email exists, reset link sent")

# ========================== PASSWORD RESET CONFIRM ============================
class PasswordResetConfirmViewAPI(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return success("Password reset successful")

# ========================== RESEND VERIFICATION EMAIL ============================
class ResendVerificationEmailViewAPI(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ResendVerificationEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = serializer.save()

        return success(result.get("message", "Email sent"))