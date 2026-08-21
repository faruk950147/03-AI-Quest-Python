from decimal import Decimal

from django.db.models import Avg, Q, Sum, Max, Min, Value, Prefetch
from django.db.models.functions import Coalesce

from store.models import (
    Category,
    Product,
    Brand,
    StatusChoices,
    VariantOption,
    Review,
    Gallery
)


def store_context(request):

    # CATEGORY QUERY
    categories = (
        Category.objects
        .filter(parent=None, status=StatusChoices.Active)
        .prefetch_related(
            Prefetch(
                "children",
                queryset=Category.objects.filter(status=StatusChoices.Active)
            ),
            Prefetch(
                "children__children",
                queryset=Category.objects.filter(status=StatusChoices.Active)
            )
        )
    )

    # PRODUCT QUERY
    products = (
        Product.objects.filter(status=StatusChoices.Active).annotate(
            total_variant_stock=Coalesce(
                Sum("variants__stock",
                    filter=Q(variants__status=StatusChoices.Active)), Value(0)),
            avg_rate=Coalesce(
                Avg("reviews__rating",
                    filter=Q(reviews__status=StatusChoices.Active)), Value(Decimal("0.0")))
        )
        .filter(
            Q(stock__gt=0) | Q(variants__stock__gt=0, 
            variants__status=StatusChoices.Active))
        .distinct()
        .select_related("category", "brand")
        .prefetch_related(Prefetch("variants",
                queryset=VariantOption.objects.filter(
                    status=StatusChoices.Active
                ).select_related("size", "color")
            ),
            Prefetch( "reviews",
                queryset=Review.objects.filter(
                    status=StatusChoices.Active
                )
            ),
            Prefetch("galleries",
                queryset=Gallery.objects.filter(
                    status=StatusChoices.Active
                ))))

    # ACTIVE CATEGORIES
    cats = (
        Category.objects
        .filter(status=StatusChoices.Active, products__status=StatusChoices.Active)
        .distinct())

    # FEATURED BRANDS
    brands = (
        Brand.objects
        .filter(
            products__in=products,
            is_featured=True
        )
        .distinct()
    )

    # PRICE RANGE
    prices = products.aggregate(
        max_price=Coalesce(
            Max("sale_price"),
            Value(Decimal("0.00"))
        ),
        min_price=Coalesce(
            Min("sale_price"),
            Value(Decimal("0.00"))
        )
    )

    return {
        "categories": categories,
        "products": products,
        "cats": cats,
        "brands": brands,
        "max_price": prices["max_price"],
        "min_price": prices["min_price"],
    }