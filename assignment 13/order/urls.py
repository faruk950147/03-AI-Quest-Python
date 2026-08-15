from django.urls import path

from order.views import(
    CheckoutView, AddressView, OrderView
)
urlpatterns = [
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('order/', OrderView.as_view(), name='order'),
    path('address/', AddressView.as_view(), name='address'),
]