from django.urls import path
from account.views import SignupView, SignInView
urlpatterns = [
    path('sign_up/', SignupView.as_view(), name='sign_up'),
    path('sign_in/', SignupView.as_view(), name='sign_in'),
]