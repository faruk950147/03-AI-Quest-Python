from store.management.commands import products
from store.models import Category, Product, Brand
from django.db.models import Avg, Q, Sum, F, Max, Min

# =========================================================
# CONTEXT PROCESSOR
# =========================================================
def store_context(request):
    # Root categories + prefetch children (2 levels)
    categories = Category.objects.filter(parent=None, status='active').prefetch_related(
        'children', 'children__children'
    )

    # Products queryset only active products with stock
    products = Product.objects.filter(status='active').annotate(
        total_variant_stock=Sum('variants__available_stock', filter=Q(variants__status='active'))
    ).filter(Q(available_stock__gt=0) | Q(total_variant_stock__gt=0))

    # Categories linked to products
    cats = Category.objects.filter(
        products__status='active'
    ).distinct().order_by('id')

    # Brands linked to products
    brands = Brand.objects.filter(
        products__status='active',
        is_featured=True
    ).distinct().order_by('id')

    # Price range
    prices = products.aggregate(max_price=Max('sale_price'), min_price=Min('sale_price'))
    max_price = prices['max_price'] or 0
    min_price = prices['min_price'] or 0

    return {
        'categories': categories,
        'cats': cats,
        'brands': brands,
        'max_price': max_price,
        'min_price': min_price
    }
