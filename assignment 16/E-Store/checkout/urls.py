# checkout/urls.py

from django.urls import path
from checkout.views import (
    ShippingView, ShippingEditView, CheckoutView,
    CheckoutPlaceView, CheckoutSuccess, CheckoutListsView
)

urlpatterns = [    
    path('shipping/add/', ShippingView.as_view(), name='shipping-add'),
    path('shipping/edit/<int:id>/', ShippingEditView.as_view(), name='shipping-edit'),
    path('view/', CheckoutView.as_view(), name='checkout-view'), 
    path('place/', CheckoutPlaceView.as_view(), name='checkout-place'),
    path('success/<int:id>/', CheckoutSuccess.as_view(), name='checkout-success'),
    path('list/', CheckoutListsView.as_view(), name='checkout-list'),
]