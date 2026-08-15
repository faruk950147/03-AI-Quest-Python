from django.urls import path

from order.views import(
    CheckoutView, OrderView
)
urlpatterns = [
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('order/', OrderView.as_view(), name='order'),
]