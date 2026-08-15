from django.shortcuts import render
from django.views import generic
# Create your views here.
class AddToCartView(generic.View):
    def post(self, request):
        # Logic to add item to cart
        pass

class CartDetailView(generic.View):
    def get(self, request):
        # Logic to display cart details
        return render(request, 'cart/cart-detail.html')
