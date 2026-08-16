from decimal import Decimal, ROUND_HALF_UP
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.db import transaction
from django.db.models import Sum, F, DecimalField
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

from cart.models import Cart
from checkout.models import Checkout, CheckoutItem, Coupon
from account.models import Shipping

SHIPPING_COST = Decimal('150.00')


# ===========================
# Checkout Page + Coupon Apply
# ===========================
@method_decorator(never_cache, name='dispatch')
class CheckoutView(LoginRequiredMixin, generic.View):
    login_url = 'sign-in'

    def get(self, request):
        cart_items = Cart.objects.filter(user=request.user, paid=False).select_related('product', 'variant')

        # Aggregate subtotal
        subtotal_dict = cart_items.aggregate(
            total=Sum(F('stored_unit_price') * F('quantity'), output_field=DecimalField(max_digits=10, decimal_places=2))
        )
        subtotal = subtotal_dict['total'] or Decimal('0.00')
        subtotal = subtotal.quantize(Decimal('0.01'), ROUND_HALF_UP)

        # Coupon handling
        discount_amount = Decimal('0.00')
        coupon_code = request.session.get('coupon_code')
        if coupon_code:
            try:
                coupon = Coupon.objects.get(code=coupon_code)
                valid, _ = coupon.is_valid(user=request.user)
                if valid:
                    discount_amount = coupon.calculate_discount(subtotal)
                else:
                    request.session.pop('coupon_code', None)
                    coupon_code = None
            except Coupon.DoesNotExist:
                request.session.pop('coupon_code', None)
                coupon_code = None

        grand_total = max(subtotal + SHIPPING_COST - discount_amount, Decimal('0.00')).quantize(Decimal('0.01'), ROUND_HALF_UP)

        shipping_address = Shipping.objects.filter(user=request.user)
        payment_methods = Checkout.PAYMENT_METHOD_CHOICES

        return render(request, 'checkout/checkout.html', {
            "cart_items": cart_items,
            "shipping_address": shipping_address,
            "payment_methods": payment_methods,
            "subtotal": subtotal,
            "shipping_cost": SHIPPING_COST,
            "discount_amount": discount_amount,
            "grand_total": grand_total,
            "coupon_code": coupon_code
        })

    def post(self, request):
        """AJAX Apply Coupon"""
        code = request.POST.get('coupon_code')
        cart_items = Cart.objects.filter(user=request.user, paid=False)
        if not cart_items.exists():
            return JsonResponse({"status": "error", "message": "Cart is empty."})

        coupon = get_object_or_404(Coupon, code=code)
        valid, message = coupon.is_valid(user=request.user)
        if not valid:
            return JsonResponse({"status": "error", "message": message})

        # Aggregate subtotal directly
        subtotal_dict = cart_items.aggregate(
            total=Sum(F('stored_unit_price') * F('quantity'), output_field=DecimalField(max_digits=10, decimal_places=2))
        )
        subtotal = subtotal_dict['total'] or Decimal('0.00')
        subtotal = subtotal.quantize(Decimal('0.01'), ROUND_HALF_UP)

        discount_amount = coupon.calculate_discount(subtotal)
        grand_total = max(subtotal + SHIPPING_COST - discount_amount, Decimal('0.00')).quantize(Decimal('0.01'), ROUND_HALF_UP)

        request.session['coupon_code'] = coupon.code
        request.session['discount_amount'] = str(discount_amount)

        return JsonResponse({
            "status": "success",
            "message": f"Coupon {coupon.code} applied!",
            "subtotal": str(subtotal),
            "discount_amount": str(discount_amount),
            "grand_total": str(grand_total)
        })


# ===========================
# Checkout Place View
# ===========================
@method_decorator(never_cache, name='dispatch')
class CheckoutPlaceView(LoginRequiredMixin, generic.View):

    def post(self, request):
        cart_items = Cart.objects.filter(user=request.user, paid=False).select_related('product', 'variant')
        if not cart_items.exists():
            return JsonResponse({"status": "error", "message": "Cart is empty."})

        shipping_id = request.POST.get("address")
        payment_method = request.POST.get("payment_method")
        coupon_code = request.POST.get("coupon_code")

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

        return JsonResponse({
            "status": "success",
            "message": "Checkout successful",
            "checkout_id": checkout.id
        })


# ===========================
# Checkout Success Page
# ===========================
@method_decorator(never_cache, name='dispatch')
class CheckoutSuccess(LoginRequiredMixin, generic.View):
    login_url = 'sign-in'

    def get(self, request, id):
        checkout = get_object_or_404(
            Checkout.objects.prefetch_related('items__product', 'items__variant'),
            id=id,
            user=request.user
        )
        return render(request, 'checkout/checkout-success.html', {"checkout": checkout})


# ===========================
# Checkout Lists Page
# ===========================
@method_decorator(never_cache, name='dispatch')
class CheckoutListsView(LoginRequiredMixin, generic.View):
    login_url = 'sign-in'

    def get(self, request):
        checkouts = Checkout.objects.filter(user=request.user)\
            .prefetch_related('items__product', 'items__variant')\
            .order_by('-created_at')
        return render(request, 'checkout/checkout-lists.html', {"checkouts": checkouts})
