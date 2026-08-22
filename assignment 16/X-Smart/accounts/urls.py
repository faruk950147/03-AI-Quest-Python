from django.urls import path
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views
from accounts.views import (
    SignUpView,
    # SignInView, 
    # SignOutView, 
    # PasswordChangeView, 
    # PasswordResetView,
    ProfileView,
    AddressView
)
from accounts.forms import SignInForm, ChangePasswordForm, PasswordResetForm, SetPasswordForm

urlpatterns = [
    path('sign-up/', SignUpView.as_view(), name='sign-up'),
    # The custom SignInView and SignOutView are commented out in favor of using Django's built-in auth views with custom forms and templates.
    # path('sign-in/', SignInView.as_view(), name='sign-in'),
    # path('sign-out/', SignOutView.as_view(), name='sign-out'),
    # path('password-change/', PasswordChangeView.as_view(), name='password-change'),
    # probational way using django built-in auth views
     path('sign-in/', auth_views.LoginView.as_view(
        template_name='accounts/sign-in.html', 
        authentication_form=SignInForm
    ), name='sign-in'),

    path('sign-out/', auth_views.LogoutView.as_view(next_page='sign-in'), name='sign-out'),

    path('password-change/', auth_views.PasswordChangeView.as_view(
        template_name='accounts/password-change.html',
        form_class=ChangePasswordForm,
        success_url='/accounts/profile/'
        # it's working fine with success_url like this also
        # success_url=reverse_lazy('password-change-done')
    ), name='password-change'),

    # path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(
    #     template_name='accounts/password-change-done.html'
    # ), name='password-change-done'),

    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='accounts/password-reset.html', 
        form_class=PasswordResetForm,
        ), name='password_reset'),    
    path(
        'password-reset-done/',
        auth_views.PasswordResetDoneView.as_view(template_name='accounts/password-reset-done.html'),
        name='password_reset_done'
    ),
    path(
        'password-reset-confirm/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='accounts/password-reset-confirm.html', form_class=SetPasswordForm),
        name='password_reset_confirm'
    ),
    path(
        'password-reset-complete/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='accounts/password-reset-complete.html',
        ),
        name='password_reset_complete'
    ),

    path('profile/', ProfileView.as_view(), name='profile'),
    path('address/', AddressView.as_view(), name='address'),
]
