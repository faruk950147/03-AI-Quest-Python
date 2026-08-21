from django.urls import path
from cart.api_views import (
    APIRoot,
    AddToCartApiView,
    CartDetailApiView,
    QuantityIncDecApiView,
    CartRemoveApiView,
    AddToWishlistApiView,
    WishlistApiView,
    WishRemoveApiView,
)

urlpatterns = [
    # =========================
    # API Root
    # =========================
    path("", APIRoot.as_view()),

    # =========================
    # Cart APIs
    # =========================
    path("add/to/", AddToCartApiView.as_view()),
    path("detail/view/", CartDetailApiView.as_view()),
    path("quantity/inc-dec/", QuantityIncDecApiView.as_view()),
    path("remove/view", CartRemoveApiView.as_view()),

    # =========================
    # Wishlist APIs
    # =========================
    path("wishlist/add/to/", AddToWishlistApiView.as_view()),
    path("wishlist/view/", WishlistApiView.as_view()),
    path("wishlist/remove/view/", WishRemoveApiView.as_view()),
]