from django.urls import path
from cart.views import (
    AddToCartView, CartDetailView, QuantityIncDec, CartRemoveView, 
    AddToWishlistView, WishRemoveView
)

urlpatterns = [
    path('add-to-cart/', AddToCartView.as_view(), name='add-to-cart'),
    path("cart-detail/", CartDetailView.as_view(), name="cart-detail"),
    path("qty-inc-dec/", QuantityIncDec.as_view(), name="qty-inc-dec"),
    path("cart-remove-item/", CartRemoveView.as_view(), name="cart-remove-item"),
    path('add-to-wish/', AddToWishlistView.as_view(), name='add-to-wish'),
    path('wish-remove-item/', WishRemoveView.as_view(), name='wish-remove-item'),
]
