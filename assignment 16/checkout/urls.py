from django.urls import path

from checkout.views import (
    CheckoutView,
    CheckoutSuccessView,
    CheckoutListView,
)
urlpatterns = [
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('checkout-success/', CheckoutSuccessView.as_view(), name='checkout-success'),
    path('checkout-list/', CheckoutListView.as_view(), name='checkout-list'),
]