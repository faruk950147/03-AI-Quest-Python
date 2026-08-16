# urls.py
from django.urls import path
from checkout.views import (
    CheckoutView, CheckoutPlaceView, CheckoutSuccess, 
    CheckoutListsView
)

urlpatterns = [
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('checkout-place/', CheckoutPlaceView.as_view(), name='checkout-place'),
    path('checkout-success/<int:id>/', CheckoutSuccess.as_view(), name='checkout-success'),
    path('checkout-list', CheckoutListsView.as_view(), name='checkout-list')   
]
