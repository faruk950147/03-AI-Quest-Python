from decimal import Decimal

from django.db.models import F, Sum, DecimalField, ExpressionWrapper

from cart.models import Cart, Wishlist


SHIPPING_COST = Decimal("150.00")


def cart_context(request):
    if not request.user.is_authenticated:
        return {
            "cart_items": [],
            "cart_count": 0,
            "wish_count": 0,
            "shipping_cost": Decimal("0.00"),
            "total_price": Decimal("0.00"),
            "grand_total": Decimal("0.00"),
        }

    cart_items = (
        Cart.objects.filter(user=request.user, paid=False)
        .select_related("product", "variant")
        .prefetch_related("product__galleries")
    )

    item_total_expression = ExpressionWrapper(
        F("quantity") * F("stored_unit_price"),
        output_field=DecimalField(max_digits=12, decimal_places=2),
    )

    total_agg = cart_items.aggregate(total=Sum(item_total_expression))

    subtotal = Decimal(total_agg["total"] or "0.00").quantize(Decimal("0.01"))

    cart_count = cart_items.count() or 0

    wish_count = (
        Wishlist.objects.filter(user=request.user).count() or 0
    )

    grand_total = (subtotal + SHIPPING_COST).quantize(Decimal("0.01"))

    return {
        "cart_items": cart_items,
        "cart_count": cart_count,
        "wish_count": wish_count,
        "shipping_cost": SHIPPING_COST,
        "subtotal": subtotal,
        "grand_total": grand_total,
    }