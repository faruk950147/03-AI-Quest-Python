from django.urls import path

from checkout.api_views import (
    CheckoutApiView,
    CheckoutPlaceApiView,
    CheckoutSuccessApiView,
    CheckoutListsApiView,
)

urlpatterns = [
    path("view/", CheckoutApiView.as_view()),
    path("place/", CheckoutPlaceApiView.as_view()),
    path("success/<int:id>/", CheckoutSuccessApiView.as_view()),
    path("list/", CheckoutListsApiView.as_view()),
]