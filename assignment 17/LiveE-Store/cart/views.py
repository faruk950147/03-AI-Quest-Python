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
@method_decorator(never_cache, name='dispatch')
class AddToCartView(LoginRequiredMixin, generic.View):
    login_url = reverse_lazy('login')

    def post(self, request):
        product_id = request.POST.get("product-id")
        product_slug = request.POST.get("product-slug")
        variant_id = request.POST.get("variant-id")
        quantity = int(request.POST.get("quantity", "1"))

        logger.info(f"AddToCart: user={request.user.username}, product_id={product_id}")

        if not product_id or quantity < 1:
            return JsonResponse({"status": "error", "message": "Invalid input."})

        with transaction.atomic():
            product = get_object_or_404(
                Product.objects.select_for_update().prefetch_related('galleries'),
                id=product_id,
                slug=product_slug,
                status=StatusChoices.Active
            )

            variant = None
            if product.variants_type != VariantType.NONE:
                if not variant_id:
                    return JsonResponse({"status": "error", "message": "Please select a variant."})

                variant = get_object_or_404(
                    VariantOption.objects.select_for_update(),
                    id=variant_id,
                    product=product,
                    status=StatusChoices.Active
                )

            max_stock = variant.stock if variant else product.stock

            if max_stock <= 0:
                return JsonResponse({"status": "error", "message": "Out of stock"})

            temp_cart = Cart(user=request.user, product=product, variant=variant)
            unit_price = temp_cart.unit_price

            cart_item, created = Cart.objects.get_or_create(
                user=request.user,
                product=product,
                variant=variant,
                paid=False,
                defaults={"quantity": quantity, "stored_unit_price": unit_price}
            )

            if not created:
                new_qty = cart_item.quantity + quantity

                if new_qty > max_stock:
                    return JsonResponse({"status": "error", "message": f"Cannot exceed stock ({max_stock})"})

                cart_item.quantity = new_qty
                cart_item.save()
                final_qty = new_qty
            else:
                if quantity > max_stock:
                    return JsonResponse({"status": "error", "message": f"Cannot exceed stock ({max_stock})"})
                final_qty = quantity

            summary = Cart.objects.filter(user=request.user, paid=False).aggregate(
                subtotal=Sum(F('quantity') * F('stored_unit_price'))
            )

            subtotal = Decimal(summary['subtotal'] or 0).quantize(Decimal('0.01'))
            cart_count = Cart.objects.filter(user=request.user, paid=False).count()

            image = (
                variant.image if variant and getattr(variant, 'image', None)
                else (product.galleries.first().image if product.galleries.exists() else "/media/defaults/default.jpg")
            )

            return JsonResponse({
                "status": "success",
                "quantity": final_qty,
                "cart_count": cart_count,
                "subtotal": str(subtotal),
                "grand_total": str((subtotal + SHIPPING_COST).quantize(Decimal('0.01'))),
                "image_url": str(image),
                "message": "Add to cart successfully"
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
                else:
                    return JsonResponse({"status": "error", "message": "Max stock reached"})

            elif action == "dec":
                if cart_item.quantity > 1:
                    cart_item.quantity -= 1
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
                "message": "Quantity changes successfully"
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
            request,
            "cart/wishlist.html",
            {
                "wish_items": wish_items,
                "wish_count": wish_items.count(),
            },
        )

    def post(self, request):
        product_id = request.POST.get("product_id")
        product_slug = request.POST.get("product_slug")

        product = get_object_or_404(
            Product,
            id=product_id,
            slug=product_slug,
            status=StatusChoices.Active,
        )

        item, created = Wishlist.objects.get_or_create(
            user=request.user,
            product=product,
        )

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
            "wish_count": Wishlist.objects.filter(
                user=request.user
            ).count(),
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