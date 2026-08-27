from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.db import transaction
from django.db.models import F, Sum
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from decimal import Decimal
import logging

from store.models import Product, VariantOption, StatusChoices, VariantType
from cart.models import Cart, Wishlist

SHIPPING_COST = Decimal('150.00')

logger = logging.getLogger('project')


# ===========================
# Add to Cart
# ===========================
@method_decorator(never_cache, name="dispatch")
class AddToCartView(LoginRequiredMixin, generic.View):
    login_url = reverse_lazy("login")

    def post(self, request):
        product_id = request.POST.get("product-id")
        product_slug = request.POST.get("product-slug")
        variant_id = request.POST.get("variant-id")
        quantity = int(request.POST.get("quantity", "1"))
        
        print(
            f"product id: {product_id} =====================",
            f"product slug: {product_slug} ====================",
            f"variant id {variant_id} =======================",
            f"Quantity: {quantity} ================================"
        )

        # logger.info(
        #     f"AddToCart: user={request.user.username}, " f"product_id={product_id}, " 
        #     f"variant_id={variant_id}, "f"quantity={quantity}"
        # )

        if not product_id or quantity < 1:
            return JsonResponse({"status": "error", "message": "Invalid input."}, status=400)


        return JsonResponse({
            "status": "success",
            "message": "Added to cart successfully."
        })


# ===========================
# Cart Detail
# ===========================
@method_decorator(never_cache, name='dispatch')
class CartDetailView(LoginRequiredMixin, generic.View):
    login_url = reverse_lazy('login')

    def get(self, request):
        cart_items = Cart.objects.filter(user=request.user, paid=False)\
            .select_related('product', 'variant')\
            .prefetch_related('product__galleries')

        summary = cart_items.aggregate(
            subtotal=Sum(F('quantity') * F('stored_unit_price'))
        )

        subtotal = Decimal(summary['subtotal'] or 0).quantize(Decimal('0.01'))

        return render(request, "cart/cart-detail.html", {
            "cart_items": cart_items,
            "subtotal": subtotal,
            "grand_total": subtotal + SHIPPING_COST
        })


# ===========================
# Quantity Increment / Decrement
# ===========================
@method_decorator(never_cache, name='dispatch')
class QuantityIncDec(LoginRequiredMixin, generic.View):
    login_url = reverse_lazy('login')

    def post(self, request):
        cart_id = request.POST.get("cart_id")
        action = request.POST.get("action")

        with transaction.atomic():
            cart_item = get_object_or_404(
                Cart.objects.select_for_update(),
                id=cart_id,
                user=request.user,
                paid=False
            )

            max_stock = cart_item.variant.stock if cart_item.variant else cart_item.product.stock

            if action == "inc":
                if cart_item.quantity < max_stock:
                    cart_item.quantity += 1
                    message = "Quantity increased"
                else:
                    return JsonResponse({"status": "error", "message": "Max stock reached"})

            elif action == "dec":
                if cart_item.quantity > 1:
                    cart_item.quantity -= 1
                    message = "Quantity decreased"
                else:
                    return JsonResponse({"status": "error", "message": "Min quantity is 1"})

            cart_item.save()

            summary = Cart.objects.filter(user=request.user, paid=False).aggregate(
                subtotal=Sum(F('quantity') * F('stored_unit_price'))
            )

            subtotal = Decimal(summary['subtotal'] or 0).quantize(Decimal('0.01'))
            cart_count = Cart.objects.filter(user=request.user, paid=False).count()

            return JsonResponse({
                "status": "success",
                "quantity": cart_item.quantity,
                "item_total": str(cart_item.subtotal),
                "subtotal": str(subtotal),
                "grand_total": str(subtotal + SHIPPING_COST),
                "cart_count": cart_count,
                "message": message
            })


# ===========================
# Remove Cart Item
# ===========================
@method_decorator(never_cache, name='dispatch')
class CartRemoveView(LoginRequiredMixin, generic.View):
    login_url = reverse_lazy('login')

    def post(self, request):
        cart_item = get_object_or_404(
            Cart,
            id=request.POST.get("cart_id"),
            user=request.user,
            paid=False
        )

        cart_item.delete()

        summary = Cart.objects.filter(user=request.user, paid=False).aggregate(
            subtotal=Sum(F('quantity') * F('stored_unit_price'))
        )

        subtotal = Decimal(summary['subtotal'] or 0).quantize(Decimal('0.01'))
        cart_count = Cart.objects.filter(user=request.user, paid=False).count()

        return JsonResponse({
            "status": "success",
            "subtotal": str(subtotal),
            "grand_total": str(subtotal + SHIPPING_COST),
            "cart_count": cart_count,
            "message": "Cart removed successfully"
        })


# ===========================
# Wishlist
# ===========================
@method_decorator(never_cache, name="dispatch")
class AddToWishlistView(LoginRequiredMixin, generic.View):
    login_url = reverse_lazy("login")

    def get(self, request):
        wish_items = (
            Wishlist.objects
            .filter(user=request.user)
            .select_related("product")
            .prefetch_related("product__galleries")
        )

        return render(
            request, "cart/wishlist.html", {"wish_items": wish_items, "wish_count": wish_items.count(),},
        )

    def post(self, request):
        product_id = request.POST.get("product_id")
        product_slug = request.POST.get("product_slug")

        product = get_object_or_404(
            Product, id=product_id, slug=product_slug, status=StatusChoices.Active,
        )

        item, created = Wishlist.objects.get_or_create(user=request.user, product=product)

        if created:
            status = "added"
            message = "Added to wishlist"
        else:
            item.delete()
            status = "removed"
            message = "Removed from wishlist"

        return JsonResponse({
            "status": status,
            "message": message,
            "wish_count": Wishlist.objects.filter(user=request.user).count(),
        })


# ===========================
# Remove Wishlist Item
# ===========================
@method_decorator(never_cache, name="dispatch")
class WishRemoveView(LoginRequiredMixin, generic.View):
    login_url = reverse_lazy("login")

    def post(self, request):
        wish_item = get_object_or_404(
            Wishlist,
            id=request.POST.get("wish_id"),
            user=request.user,
        )

        wish_item.delete()

        return JsonResponse({
            "status": "success",
            "message": "Removed from wishlist",
            "wish_count": Wishlist.objects.filter(
                user=request.user
            ).count(),
        })