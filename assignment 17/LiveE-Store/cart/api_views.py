from django.shortcuts import get_object_or_404
from django.db import transaction
from django.db.models import F, Sum
from django.contrib.auth import get_user_model

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from decimal import Decimal

from store.models import Product, VariantOption, StatusChoices, VariantType
from cart.models import Cart, Wishlist
from cart.serializers import CartSerializer, WishlistSerializer

User = get_user_model()

SHIPPING_COST = Decimal('150.00')


def success(message, data=None, code=200):
    return Response(
        {
            "success": True,
            "message": message,
            "data": data
        },
        status=code
    )

def error(message, code=400):
    return Response(
        {
            "success": False,
            "message": message
        },
        status=code
    )

# ========================= 
# API ROOT 
# =========================
class APIRoot(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        return Response({
            "add_to_cart": "http://127.0.0.1:8000/api/cart/add/to/",
            "cart_detail": "http://127.0.0.1:8000/api/cart/detail/view/",
            "cart_quantity_update": "http://127.0.0.1:8000/api/cart/quantity/inc-dec/",
            "cart_remove": "http://127.0.0.1:8000/api/cart/remove/view",
            "wishlist_add": "http://127.0.0.1:8000/api/cart/wishlist/add/to/",
            "wishlist_detail": "http://127.0.0.1:8000/api/cart/wishlist/view/",
            "wishlist_remove": "http://127.0.0.1:8000/api/cart/wishlist/remove/view/"
        })

# =========================
# Add to Cart View
# =========================
class AddToCartApiView(APIView):
    def post(self, request):
        product_id = request.data.get("product_id")
        product_slug = request.data.get("product_slug")
        variant_id = request.data.get("variant_id")
        quantity = int(request.data.get("quantity", 1))

        if not product_id or quantity < 1:
            return error("Invalid product ID or quantity.")

        with transaction.atomic():
            product = get_object_or_404(
                Product.objects.select_for_update().prefetch_related("galleries"),
                id=product_id,
                slug=product_slug,
                status=StatusChoices.Active
            )

            variant = None

            if product.variants_type != VariantType.NONE:
                if not variant_id:
                    return error("Please select a variant.")

                variant = get_object_or_404(
                    VariantOption.objects.select_for_update(),
                    id=variant_id,
                    product=product,
                    status=StatusChoices.Active
                )

            max_stock = variant.stock if variant else product.stock

            if max_stock <= 0:
                return error("Out of stock")

            temp_cart = Cart(user=request.user, product=product, variant=variant)

            unit_price = temp_cart.unit_price
            
            cart_item, created = Cart.objects.get_or_create(
                user=request.user,
                product=product,
                variant=variant,
                paid=False,
                defaults={
                    "quantity": quantity,
                    "stored_unit_price": unit_price
                })

            if not created:
                new_qty = cart_item.quantity + quantity
                if new_qty > max_stock:
                    return error(f"Cannot exceed stock ({max_stock})")
                cart_item.quantity = new_qty
                cart_item.save()

                final_qty = new_qty
            else:
                if quantity > max_stock:
                    return error(f"Cannot exceed stock ({max_stock})")
                final_qty = quantity

            summary = Cart.objects.filter(user=request.user, paid=False
            ).aggregate(subtotal=Sum(F("quantity") * F("stored_unit_price")))

            subtotal = Decimal(summary["subtotal"] or 0).quantize(Decimal("0.01"))
            grand_total = (subtotal + SHIPPING_COST).quantize(Decimal("0.01"))
            cart_count = Cart.objects.filter(user=request.user, paid=False).count()

            image = (
                variant.image
                if variant and getattr(variant, "image", None)
                else (
                    product.galleries.first().image
                    if product.galleries.exists()
                    else "/media/default.jpg"
                )
            )

            return success(
                "Product added to cart successfully.",
                {
                    "quantity": final_qty,
                    "cart_count": cart_count,
                    "subtotal": str(subtotal),
                    "grand_total": str(grand_total),
                    "image_url": str(image),
                }
            )

# =========================
# Cart Detail View
# =========================
class CartDetailApiView(APIView):
    def get(self, request):
        cart_items = (
            Cart.objects.filter(user=request.user, paid=False)
            .select_related("product", "variant")
            .prefetch_related("product__galleries")
        )

        summary = cart_items.aggregate(
            subtotal=Sum(F("quantity") * F("stored_unit_price"))
        )

        subtotal = Decimal(summary["subtotal"] or 0).quantize(Decimal("0.01"))
        grand_total = (subtotal + SHIPPING_COST).quantize(Decimal("0.01"))

        data = {
            "cart_items": CartSerializer(cart_items, many=True).data,
            "cart_count": cart_items.count(),
            "subtotal": str(subtotal),
            "shipping_cost": str(SHIPPING_COST),
            "grand_total": str(grand_total),
        }

        return success(
            "Cart details retrieved successfully.",
            data
        )

# ===========================
# Quantity Increment / Decrement
# ===========================
class QuantityIncDecApiView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        cart_id = request.data.get("cart_id")
        action = request.data.get("action")

        with transaction.atomic():
            cart_item = get_object_or_404(
                Cart.objects.select_for_update(),
                id=cart_id,
                user=request.user,
                paid=False
            )

            max_stock = (
                cart_item.variant.stock
                if cart_item.variant
                else cart_item.product.stock
            )

            if action == "inc":
                if cart_item.quantity < max_stock:
                    cart_item.quantity += 1
                else:
                    return error("Max stock reached")

            elif action == "dec":
                if cart_item.quantity > 1:
                    cart_item.quantity -= 1
                else:
                    return error("Minimum quantity is 1")

            else:
                return error("Invalid action")

            cart_item.save()

            summary = Cart.objects.filter(
                user=request.user,
                paid=False
            ).aggregate(
                subtotal=Sum(F("quantity") * F("stored_unit_price"))
            )

            subtotal = Decimal(summary["subtotal"] or 0).quantize(Decimal("0.01"))
            grand_total = (subtotal + SHIPPING_COST).quantize(Decimal("0.01"))
            cart_count = Cart.objects.filter(
                user=request.user,
                paid=False
            ).count()

            data = {
                "cart_items": CartSerializer(
                    Cart.objects.filter(user=request.user, paid=False),
                    many=True
                ).data,
                "quantity": cart_item.quantity,
                "item_total": str(cart_item.subtotal),
                "subtotal": str(subtotal),
                "grand_total": str(grand_total),
                "cart_count": cart_count,
            }

        return success("Quantity updated successfully.", data)

# ==========================
# Remove Item from Cart
# ==========================
class CartRemoveApiView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        cart_id = request.data.get("cart_id")

        cart_item = get_object_or_404(
            Cart,
            id=cart_id,
            user=request.user,
            paid=False
        )

        cart_item.delete()

        summary = Cart.objects.filter(
            user=request.user,
            paid=False
        ).aggregate(
            subtotal=Sum(F("quantity") * F("stored_unit_price"))
        )

        subtotal = Decimal(summary["subtotal"] or 0).quantize(Decimal("0.01"))
        grand_total = (subtotal + SHIPPING_COST).quantize(Decimal("0.01"))
        cart_count = Cart.objects.filter(
            user=request.user,
            paid=False
        ).count()

        data = {
            "cart_count": cart_count,
            "subtotal": str(subtotal),
            "shipping_cost": str(SHIPPING_COST),
            "grand_total": str(grand_total),
        }

        return success(
            "Item removed from cart successfully.",
            data
        )

# ===========================
# Add to Wishlist View
# ===========================
class AddToWishlistApiView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        product_id = request.data.get("product_id")
        product_slug = request.data.get("product_slug")
        variant_id = request.data.get("variant_id")

        if not product_id:
            return error("Product ID is required.")

        product = get_object_or_404(
            Product,
            id=product_id,
            slug=product_slug,
            status=StatusChoices.Active
        )

        variant = None
        if variant_id:
            variant = get_object_or_404(
                VariantOption,
                id=variant_id,
                product=product,
                status=StatusChoices.Active
            )

        wishlist_item, created = Wishlist.objects.get_or_create(
            user=request.user,
            product=product,
            variant=variant
        )

        if not created:
            return error("Product already exists in wishlist.")

        data = {
            "wishlist_count": Wishlist.objects.filter(user=request.user).count()
        }

        return success("Product added to wishlist successfully.", data)
    
# ===========================
# Wishlist View
# ===========================
class WishlistApiView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        wishlist = Wishlist.objects.filter(user=request.user)

        data = {
            "wishlist_items": WishlistSerializer(wishlist, many=True).data,
            "wishlist_count": wishlist.count(),
        }

        return success("Wishlist retrieved successfully.", data)
        
# ===========================
# Remove Wishlist Item
# ===========================
class WishRemoveApiView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        wish_item = get_object_or_404(
            Wishlist,
            id=request.data.get("wish_id"),
            user=request.user
        )

        wish_item.delete()

        wishlist = Wishlist.objects.filter(user=request.user)

        data = {
            "wishlist_count": wishlist.count(),
            "wishlist_items": WishlistSerializer(wishlist, many=True).data,
        }

        return success("Item removed from wishlist successfully.", data)