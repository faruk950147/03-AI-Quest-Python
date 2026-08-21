from django.urls import path
from account.views import (
    SignupView,
    VerifyEmailView,
    LoginView,
    LogoutView,
    ChangePasswordView,
    PasswordResetView,
    PasswordResetConfirmView,
    ResendVerifyEmailView,
    ProfileView
)

urlpatterns = [
    # Authentication
    path('signup/', SignupView.as_view(), name='signup'),
    path('verify/email/', VerifyEmailView.as_view(), name='verify-email'),
    path('resend/verify/email/', ResendVerifyEmailView.as_view(), name='resend-verify-email'),

    # Login & Logout
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    # Password Management
    path('change/password/', ChangePasswordView.as_view(), name='change-password'),
    path('password/reset/', PasswordResetView.as_view(), name='password-reset'),
    path('password/reset/confirm/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    
    # Profile
    path('profile/', ProfileView.as_view(), name='profile'),
]