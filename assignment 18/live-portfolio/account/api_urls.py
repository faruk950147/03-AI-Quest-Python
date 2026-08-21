from django.urls import path

from account.api_views import (
    RootAPIView,
    SignupViewAPI,
    VerifyEmailViewAPI,
    LoginViewAPI,
    LogoutViewAPI,
    ChangePasswordViewAPI,
    PasswordResetViewAPI,
    PasswordResetConfirmViewAPI,
    ResendVerifyEmailViewAPI,
)
urlpatterns = [
    path('', RootAPIView.as_view()),
    path('signup/', SignupViewAPI.as_view()),
    path('verify/email/', VerifyEmailViewAPI.as_view()),
    path('login/', LoginViewAPI.as_view()),
    path('logout/', LogoutViewAPI.as_view()),
    path('change/password/', ChangePasswordViewAPI.as_view()),
    path('password/reset/', PasswordResetViewAPI.as_view()),
    path('password/reset/confirm/', PasswordResetConfirmViewAPI.as_view()),
    path('resend/verify/email/', ResendVerifyEmailViewAPI.as_view())
]