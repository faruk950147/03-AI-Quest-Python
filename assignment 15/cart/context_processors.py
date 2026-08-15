from django.db.models import Min, Max
from cart.models import (
    Cart,
)
def get_filters(request):
    if request.user.is_authenticated:
        cart_count = Cart.objects.filter(user=request.user, paid=False)
        return {
            'cart_count': cart_count.count(),
        }
    else:
        return {}