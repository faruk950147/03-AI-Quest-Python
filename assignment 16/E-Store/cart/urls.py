from django.urls import path

from cart.views import (
    AddToCartView,
    CartDetailView,
    QuantityIncDec,
    CartRemoveView,
    AddToWishlistView,
    WishRemoveView,
)


urlpatterns = [
    # Cart
    path("add/to/", AddToCartView.as_view(), name="add-to-cart"),
    path("detail/view/", CartDetailView.as_view(), name="detail-view"),
    path("quantity/inc-dec/", QuantityIncDec.as_view(), name="quantity-inc-dec/"),
    path("remove/view/", CartRemoveView.as_view(), name="cart-remove"),

    # Wishlist
    path("wishlist/view/", AddToWishlistView.as_view(), name="wishlist"),
    path("wishlist/remove/view/", WishRemoveView.as_view(), name="wishlist-remove"),
]