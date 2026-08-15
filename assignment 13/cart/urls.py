from django.urls import path
from cart.views import (
    AddToCartView, CartDetailView,
)
urlpatterns = [
    path('add-to-cart/', AddToCartView.as_view(), name='add-to-cart'),
    path('cart-detail/', CartDetailView.as_view(), name='cart-detail'),
]