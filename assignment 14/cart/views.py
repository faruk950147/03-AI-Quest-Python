from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import generic
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from store.models import Product
from cart.models import Cart
from accounts.mixing import LoginRequiredMixin

@method_decorator(never_cache, name='dispatch')
class AddToCartView(LoginRequiredMixin, generic.View):
    login_url = reverse_lazy('sign-in')
    def post(self, request):
        # Get product ID and quantity from POST request
        product_id = request.POST.get("product-id")
        quantity = int(request.POST.get("quantity", 0))

        # Basic validation
        if not product_id or quantity < 1:
            messages.error(request, "Invalid request.")
            return redirect('home')

        # Fetch the product from the database
        product = get_object_or_404(Product, id=product_id)

        # Check stock availability
        if quantity > product.available_stock:
            messages.error(
                request,
                f"Quantity cannot exceed available stock! Maximum available: {product.available_stock}."
            )
            return redirect('single-product', slug=product.slug, id=product.id)

        # Get the user's unpaid cart items for this product as a list
        cart_items = list(Cart.objects.filter(user=request.user, product=product, paid=False))

        if cart_items:
            # Product already exists in cart, update quantity
            cart_item = cart_items[0]  # Get the first (and only) cart item
            new_quantity = cart_item.quantity + quantity

            if new_quantity <= product.available_stock:
                cart_item.quantity = new_quantity
                cart_item.save()  
                messages.success(request, "Item quantity updated successfully!")
            else:
                messages.error(request, f"You can't add more than {product.available_stock} units!")
        else:
            # Product not in cart, create a new cart item
            Cart.objects.create(user=request.user, product=product, quantity=quantity)
            messages.success(request, "Item added to cart successfully!")

        # Redirect user back to the product page
        return redirect('single-product', slug=product.slug, id=product.id)

@method_decorator(never_cache, name='dispatch')
class CartDetailView(LoginRequiredMixin, generic.View):
    login_url = reverse_lazy('sign-in')
    def get(self, request):
        # Get all unpaid cart items for the user
        cart_items = Cart.objects.filter(user=request.user, paid=False)

        # Calculate total for all cart items
        cart_total = sum(item.subtotal for item in cart_items)

        # Define shipping cost (you can make it dynamic if needed)
        shipping_cost = 50  

        context = {
            "cart_items": cart_items,
            "cart_total": cart_total,
            "shipping_cost": shipping_cost,
        }
        return render(request, 'cart/cart-detail.html', context)

class QuantityIncDec(LoginRequiredMixin, generic.View):
    login_url = reverse_lazy('sign-in')
    def post(self, request):
        cart_item_id = request.POST.get("product-id")
        action = request.POST.get("action")

        if cart_item_id and action:
            try:
                cart_item = Cart.objects.get(id=cart_item_id, user=request.user, paid=False)
                if action == "inc":
                    cart_item.quantity += 1
                    cart_item.save()
                elif action == "dec" and cart_item.quantity > 1:
                    cart_item.quantity -= 1
                    cart_item.save()

            except Cart.DoesNotExist:
                pass  # item not found, quietly ignore

        # quantity updated cart page redirect
        return redirect('cart-detail')