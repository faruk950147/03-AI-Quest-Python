from decimal import Decimal
from django.db.models import F, Sum
from cart.models import Cart, Wishlist

def cart_context(request):
    SHIPPING_COST = Decimal('150.00')  # Shipping cost can be Decimal for precision

    if request.user.is_authenticated:
        # Get all unpaid cart items with related product and variant
        cart_items = Cart.objects.filter(user=request.user, paid=False).select_related('product', 'variant')

        # Count of cart objects
        cart_count = Cart.objects.filter(user=request.user, paid=False).count()
        wish_count = Wishlist.objects.filter(user=request.user).count()
        # Aggregate total price at database level
        total_agg = cart_items.aggregate(total=Sum(F('quantity') * F('stored_unit_price')))
        total_price = Decimal(total_agg['total'] or 0).quantize(Decimal('0.01'))

        # Grand total with shipping
        grand_total = (total_price + SHIPPING_COST).quantize(Decimal('0.01'))

        return {
            'cart_items': cart_items,
            'cart_count': cart_count,
            'wish_count': wish_count,
            'shipping_cost': SHIPPING_COST,
            'total_price': total_price,
            'grand_total': grand_total
        }

    # For anonymous users
    return {
        'cart_items': [],
        'cart_count': 0,
        'wish_count': 0,
        'shipping_cost': Decimal('0.00'),
        'total_price': Decimal('0.00'),
        'grand_total': Decimal('0.00')
    }

