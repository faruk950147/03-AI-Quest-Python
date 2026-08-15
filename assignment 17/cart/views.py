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

from store.models import Product, ProductVariant
from cart.models import Cart, Wishlist

SHIPPING_COST = Decimal('150.00')
import logging

logger = logging.getLogger('project') 


# ===========================
# Add to Cart
# ===========================
@method_decorator(never_cache, name='dispatch')
class AddToCartView(LoginRequiredMixin, generic.View):
    login_url = reverse_lazy('sign-in')

    def post(self, request):
        try:
            product_id = request.POST.get("product_id")
            product_slug = request.POST.get("product_slug")
            variant_id = request.POST.get("variant_id")
            quantity = int(request.POST.get("quantity", "1"))

            logger.info(f"AddToCart requested by {request.user.username}: product_id={product_id}, variant_id={variant_id}, quantity={quantity}")

            if not product_id or quantity < 1:
                return JsonResponse({"status": "error", "message": "Invalid input."})

            with transaction.atomic():
                product = get_object_or_404(
                    Product.objects.select_for_update().prefetch_related('images'),
                    id=product_id, slug=product_slug, status='active'
                )

                variant = None
                if product.variant != 'none':
                    if not variant_id:
                        return JsonResponse({"status": "error", "message": "Please select a variant."})
                    variant = get_object_or_404(
                        ProductVariant.objects.select_for_update(),
                        id=variant_id, product=product, status='active'
                    )

                max_stock = variant.available_stock if variant else product.available_stock
                if max_stock <= 0:
                    msg = "Selected variant is out of stock." if variant else "Product is out of stock."
                    return JsonResponse({"status": "error", "message": msg})

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
                    new_quantity = cart_item.quantity + quantity
                    if new_quantity > max_stock:
                        return JsonResponse({"status": "error", "message": f"Cannot exceed stock ({max_stock})."})
                    cart_item.quantity = new_quantity
                    cart_item.save()
                    final_quantity = new_quantity
                    message = "Cart updated successfully."
                else:
                    final_quantity = quantity
                    message = "Product added to cart successfully."

                summary = Cart.objects.filter(user=request.user, paid=False).aggregate(
                    subtotal=Sum(F('quantity') * F('stored_unit_price'))
                )
                subtotal = Decimal(summary['subtotal'] or 0).quantize(Decimal('0.01'))
                cart_count = Cart.objects.filter(user=request.user, paid=False).count()

                image = variant.image if variant and getattr(variant, 'image', None) else (product.images.first().image if product.images.exists() else "/media/defaults/default.jpg")

                return JsonResponse({
                    "status": "success",
                    "message": message,
                    "product_title": product.title,
                    "unit_price": str(unit_price),
                    "quantity": final_quantity,
                    "available_stock": max_stock,
                    "cart_count": cart_count,
                    "subtotal": str(subtotal),
                    "grand_total": str((subtotal + SHIPPING_COST).quantize(Decimal('0.01'))),
                    "image_url": str(image)
                })

        except Exception as e:
            logger.error(f"AddToCart error: {e}", exc_info=True)
            return JsonResponse({"status": "error", "message": "Something went wrong. Please try again."})


# ===========================
# Cart Detail View 
# ===========================
@method_decorator(never_cache, name='dispatch')
class CartDetailView(LoginRequiredMixin, generic.View):
    login_url = reverse_lazy('sign-in')

    def get(self, request):
        try:
            logger.info(f"CartDetail requested by user={request.user.username}")

            cart_items = Cart.objects.filter(user=request.user, paid=False)\
                .select_related('product', 'variant', 'variant__color', 'variant__size')\
                .prefetch_related('product__images')

            summary = cart_items.aggregate(
                subtotal=Sum(F('quantity') * F('stored_unit_price'))
            )
            subtotal = Decimal(summary['subtotal'] or 0).quantize(Decimal('0.01'))
            grand_total = (subtotal + SHIPPING_COST).quantize(Decimal('0.01'))

            return render(request, "cart/cart-detail.html", {
                "cart_items": cart_items,
                "subtotal": subtotal,
                "grand_total": grand_total,
            })

        except Exception as e:
            logger.error(f"CartDetail error: {e}", exc_info=True)
            return render(request, "cart/cart-detail.html", {
                "cart_items": [],
                "subtotal": Decimal('0.00'),
                "grand_total": Decimal('0.00'),
                "error_message": "Unable to load cart. Please try again."
            })


# ===========================
# Quantity Increment/Decrement
# ===========================
@method_decorator(never_cache, name='dispatch')
class QuantityIncDec(LoginRequiredMixin, generic.View):
    login_url = reverse_lazy('sign-in')

    def post(self, request):
        try:
            cart_id = request.POST.get("cart_id")
            action = request.POST.get("action")
            logger.info(f"QuantityIncDec requested: cart_id={cart_id}, action={action}, user={request.user.username}")

            with transaction.atomic():
                cart_item = get_object_or_404(
                    Cart.objects.select_for_update(),
                    id=cart_id,
                    user=request.user,
                    paid=False
                )
                max_stock = cart_item.variant.available_stock if cart_item.variant else cart_item.product.available_stock

                if action == "inc":
                    if cart_item.quantity < max_stock:
                        cart_item.quantity += 1
                    else:
                        return JsonResponse({'status':'error','message':'Maximum stock reached'})
                elif action == "dec":
                    if cart_item.quantity > 1:
                        cart_item.quantity -= 1
                    else:
                        return JsonResponse({'status':'error','message':'Minimum quantity is 1'})
                else:
                    return JsonResponse({'status':'error','message':'Invalid action'})

                cart_item.save()

                summary = Cart.objects.filter(user=request.user, paid=False).aggregate(
                    subtotal=Sum(F('quantity') * F('stored_unit_price'))
                )
                subtotal = Decimal(summary['subtotal'] or 0).quantize(Decimal('0.01'))
                cart_count = Cart.objects.filter(user=request.user, paid=False).count()

                return JsonResponse({
                    "status": "success",
                    "message": "Quantity updated",
                    "quantity": cart_item.quantity,
                    "item_total": str(cart_item.subtotal),
                    "subtotal": str(subtotal),
                    "grand_total": str((subtotal + SHIPPING_COST).quantize(Decimal('0.01'))),
                    "cart_count": cart_count
                })

        except Exception as e:
            logger.error(f"QuantityIncDec error: {e}", exc_info=True)
            return JsonResponse({"status": "error", "message": "Something went wrong. Please try again."})


# ===========================
# Remove Cart Item
# ===========================
@method_decorator(never_cache, name='dispatch')
class CartRemoveView(LoginRequiredMixin, generic.View):
    login_url = reverse_lazy('sign-in')

    def post(self, request):
        cart_item = get_object_or_404(
            Cart, 
            id=request.POST.get("cart_id"), 
            user=request.user, 
            paid=False
        )
        logger.info(f"Cart Remove requested: cart_id={cart_item.id}, user={request.user.username}")

        cart_item.delete()

        summary = Cart.objects.filter(user=request.user, paid=False).aggregate(
            subtotal=Sum(F('quantity') * F('stored_unit_price'))
        )
        subtotal = Decimal(summary['subtotal'] or 0).quantize(Decimal('0.01'))
        cart_count = Cart.objects.filter(user=request.user, paid=False).count()

        return JsonResponse({
            "status": "success",
            "message": "Item removed",
            "subtotal": str(subtotal),
            "grand_total": str((subtotal + SHIPPING_COST).quantize(Decimal('0.01'))),
            "cart_count": cart_count
        })

# ===========================
# Add Wishlist Item
# ===========================
@method_decorator(never_cache, name='dispatch')
class AddToWishlistView(LoginRequiredMixin, generic.View):
    login_url = reverse_lazy('sign-in')

    def get(self, request):
        wish_items = Wishlist.objects.filter(user=request.user)\
            .select_related('product', 'variant', 'variant__color', 'variant__size')\
            .prefetch_related('product__images')
        wish_count = wish_items.count()
        return render(request, 'cart/wishlist.html', {
            'wish_items': wish_items,
            'wish_count': wish_count
        })

    def post(self, request):
        product_id = request.POST.get('product_id')
        variant_id = request.POST.get('variant_id')

        if not product_id:
            return JsonResponse({'status': 'error', 'message': 'Invalid product.'})

        product = get_object_or_404(Product, id=product_id)
        variant = None
        if variant_id:
            variant = get_object_or_404(ProductVariant, id=variant_id, product=product)

        wishlist_item, created = Wishlist.objects.get_or_create(
            user=request.user,
            product=product,
            variant=variant
        )

        if not created:
            wishlist_item.delete()
            status = 'removed'
            message = 'Removed from wishlist'
        else:
            status = 'added'
            message = 'Added to wishlist'

        wish_count = Wishlist.objects.filter(user=request.user).count()
        logger.info(f"WishlistToggle: user={request.user.username}, product_id={product_id}, variant_id={variant_id}, status={status}")

        return JsonResponse({
            'status': status,
            'message': message,
            'wish_count': wish_count
        })


# ===========================
# Remove Wishlist Item
# ===========================
@method_decorator(never_cache, name='dispatch')
class WishRemoveView(LoginRequiredMixin, generic.View):
    login_url = reverse_lazy('sign-in')

    def post(self, request):
        wish_item = get_object_or_404(
            Wishlist, 
            id=request.POST.get("wish_id"), 
            user=request.user, 
        )
        logger.info(f"Wish Remove requested: wish_id={wish_item.id}, user={request.user.username}")

        wish_item.delete()

        wish_count = Wishlist.objects.filter(user=request.user).count()
        return JsonResponse({
            "status": "success",
            "message": "Item removed",
            "wish_count": wish_count
        })