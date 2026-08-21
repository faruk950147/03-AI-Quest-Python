from django.urls import path
from account import views
urlpatterns = [
    path('signup/', views.SignupView.as_view(), name='signup'),
    path("verify/email/", views.EmailVerifyView.as_view(), name='verify-email'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('change/password/', views.ChangePasswordView.as_view(), name='change-password'),
    path('password/reset/', views.PasswordResetRequestView.as_view(), name='reset-password'),
    path('password/reset/confirm/', views.PasswordResetConfirmView.as_view(), name='reset-password-confirm'),
    path('resend/email/', views.ResendVerificationView.as_view(), name='resend-email'),
    path('profile/', views.ProfileView.as_view(), name='profile')
]