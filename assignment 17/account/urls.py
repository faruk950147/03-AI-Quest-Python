from django.urls import path
from account.views import (
    UsernameValidationView,
    EmailValidationView,   
    PasswordValidationView,
    SignInValidationView, 
    AccountActivationView,
    SignUpView,
    SignInView,
    SignOutView,
    ChangesPasswordView,
    ResetPasswordView,
    ResetPasswordConfirmView,  
    UserInfoEditView,
    ShippingAddressView,
    ShippingAddressListView,
    ShippingAddressDeleteView,
    ShippingAddressEditView,
    AccountView
)

urlpatterns = [
    path('validate-username/', UsernameValidationView.as_view(), name='validate-username'),
    path('validate-email/', EmailValidationView.as_view(), name='validate-email'),
    path('validate-password/', PasswordValidationView.as_view(), name='validate-password'),
    path('validate-signin/', SignInValidationView.as_view(), name='validate-signin'),

    path('activate-account/<uidb64>/<token>/', AccountActivationView.as_view(), name='activate-account'),

    path('sign-up/', SignUpView.as_view(), name='sign-up'),
    path('sign-in/', SignInView.as_view(), name='sign-in'),
    path('sign-out/', SignOutView.as_view(), name='sign-out'),
    path('change-password/', ChangesPasswordView.as_view(), name='change-password'),

    # Reset password flow
    path('reset-password/', ResetPasswordView.as_view(), name='reset-password'),
    path('reset-password/<uidb64>/<token>/', ResetPasswordConfirmView.as_view(), name='reset_password_confirm'),
    
    path('user-info-edit/', UserInfoEditView.as_view(), name='user-info-edit'),
    path('shipping-address/', ShippingAddressView.as_view(), name='shipping-address'),
    path('address-list/', ShippingAddressListView.as_view(), name='address-list'),
    path('address-delete/<int:id>/', ShippingAddressDeleteView.as_view(), name='address-delete'),
    path('address-edit/<int:id>/', ShippingAddressEditView.as_view(), name='address-edit'),
    path('account/', AccountView.as_view(), name='account'),
]
