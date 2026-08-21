from decimal import Decimal, ROUND_HALF_UP

from django.db import transaction
from django.db.models import F, Sum, DecimalField
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from rest_framework.response import Response
from rest_framework.views import APIView

from cart.models import Cart
from cart.serializers import CartSerializer

from checkout.serializers import (
    CouponSerializer, 
    CheckoutSerializer, 
    CheckoutItemSerializer, 
    ShippingSerializer
)
from checkout.models import (
    Coupon,
    Checkout,
    CheckoutItem,
    Shipping,
)

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

# ===========================
# Checkout API View & Coupon Apply
# ===========================
class CheckoutApiView(APIView):

    def get(self, request):
        cart_items = Cart.objects.filter(user=request.user, paid=False).select_related('product', 'variant')

        # Aggregate subtotal
        subtotal_dict = cart_items.aggregate(
            total=Sum(F('stored_unit_price') * F('quantity'), output_field=DecimalField(max_digits=10, decimal_places=2))
        )
        subtotal = subtotal_dict['total'] or Decimal('0.00')
        subtotal = subtotal.quantize(Decimal('0.01'), ROUND_HALF_UP)

        # Coupon handling from session
        discount_amount = Decimal('0.00')
        coupon_code = request.session.get('coupon_code')

        if coupon_code:
            coupon = Coupon.objects.filter(code=coupon_code).first()
            if coupon:
                valid, _ = coupon.is_valid(user=request.user)
                if valid:
                    discount_amount = coupon.calculate_discount(subtotal)
                else:
                    request.session.pop('coupon_code', None)
                    coupon_code = None
            else:
                request.session.pop('coupon_code', None)
                coupon_code = None

        grand_total = max(subtotal + SHIPPING_COST - discount_amount, Decimal('0.00')).quantize(Decimal('0.01'), ROUND_HALF_UP)

        shipping_addresses = Shipping.objects.filter(user=request.user)
        payment_methods = [
            {"value": key, "label": str(label)} for key, label in Checkout.PAYMENT_METHOD_CHOICES
        ]

        data = {
            "cart_items": CartSerializer(cart_items, many=True).data,
            "subtotal": str(subtotal),
            "shipping_cost": str(SHIPPING_COST),
            "discount_amount": str(discount_amount),
            "grand_total": str(grand_total),
            "coupon_code": coupon_code,
            "shipping_address": ShippingSerializer(shipping_addresses, many=True).data,
            "payment_methods": payment_methods
        }
        return success("Checkout details retrieved successfully.", data=data)

    def post(self, request):
        """API Apply Coupon"""
        code = request.data.get('coupon_code') or request.POST.get('coupon_code')
        
        if not code:
            return error("Coupon code is required.", code=400)

        cart_items = Cart.objects.filter(user=request.user, paid=False)
        if not cart_items.exists():
            return error("Cart is empty.", code=400)

        coupon = Coupon.objects.filter(code=code).first()
        if not coupon:
            return error("Invalid Coupon Code.", code=404)

        valid, message = coupon.is_valid(user=request.user)
        if not valid:
            return error(message, code=400)

        # Calculate updated figures
        subtotal_dict = cart_items.aggregate(
            total=Sum(F('stored_unit_price') * F('quantity'), output_field=DecimalField(max_digits=10, decimal_places=2))
        )
        subtotal = subtotal_dict['total'] or Decimal('0.00')
        subtotal = subtotal.quantize(Decimal('0.01'), ROUND_HALF_UP)

        discount_amount = coupon.calculate_discount(subtotal)
        grand_total = max(subtotal + SHIPPING_COST - discount_amount, Decimal('0.00')).quantize(Decimal('0.01'), ROUND_HALF_UP)

        # Cache session coupon variables
        request.session['coupon_code'] = coupon.code
        request.session['discount_amount'] = str(discount_amount)

        data = {
            "coupon_code": coupon.code,
            "subtotal": str(subtotal),
            "discount_amount": str(discount_amount),
            "grand_total": str(grand_total)
        }
        return success(f"Coupon {coupon.code} applied successfully!", data=data)
    

# ===========================
# Checkout Place View
# ===========================
class CheckoutPlaceApiView(APIView):

    def post(self, request):
        cart_items = Cart.objects.filter(user=request.user, paid=False).select_related('product', 'variant')
        if not cart_items.exists():
            return error("Cart is empty.", code=400)

        shipping_id = request.data.get("address")
        payment_method = request.data.get("payment_method")
        coupon_code = request.data.get("coupon_code")

        shipping = get_object_or_404(Shipping, id=shipping_id, user=request.user)

        coupon = None
        if coupon_code:
            try:
                coupon = Coupon.objects.get(code=coupon_code)
            except Coupon.DoesNotExist:
                coupon = None

        with transaction.atomic():
            checkout = Checkout.objects.create(
                user=request.user,
                shipping=shipping,
                payment_method=payment_method,
                coupon=coupon
            )

            # Create Checkout Items
            items_bulk = [
                CheckoutItem(
                    checkout=checkout,
                    product=item.product,
                    variant=item.variant,
                    quantity=item.quantity,
                    unit_price=item.stored_unit_price,
                    subtotal=(item.stored_unit_price * item.quantity).quantize(Decimal('0.01'), ROUND_HALF_UP)
                )
                for item in cart_items
            ]
            CheckoutItem.objects.bulk_create(items_bulk)

            # Finalize Checkout (stock, coupon, totals)
            checkout.finalization_checkout()

            # Clear Cart
            cart_items.delete()

            data = {
                "checkout_id": checkout.id,
                "message": "Checkout placed successfully."
            }
        return success("Checkout placed successfully.", data=data)


# ===========================
# Checkout Success API View
# ==========================
class CheckoutSuccessApiView(APIView):

    def get(self, request, id):
        checkout = get_object_or_404(
            Checkout.objects.prefetch_related('items__product', 'items__variant'),
            id=id,
            user=request.user
        )
        data={
            "checkout_id": checkout.id, 
            "shipping_address": ShippingSerializer(checkout.shipping).data,
            "payment_method": checkout.payment_method,
        }
        return success("Checkout details retrieved successfully.", data=data)
    

# ===========================
# Checkout Lists Page
# ===========================   
class CheckoutListsApiView(APIView):
    def get(self, request):
        checkouts = Checkout.objects.filter(user=request.user)\
            .prefetch_related('items__product', 'items__variant')\
            .order_by('-created_at')
        data = [
            {
                "checkout_id": checkout.id,
                "created_at": checkout.created_at,
                "shipping_address": ShippingSerializer(checkout.shipping).data,
                "payment_method": checkout.payment_method,
                "items": [
                    {
                        "product_name": item.product.name,
                        "variant_name": item.variant.name if item.variant else None,
                        "quantity": item.quantity,
                        "unit_price": str(item.unit_price),
                        "subtotal": str(item.subtotal)
                    }
                    for item in checkout.items.all()
                ]
            }
            for checkout in checkouts
        ]
        return success("Checkout lists retrieved successfully.", data=data)