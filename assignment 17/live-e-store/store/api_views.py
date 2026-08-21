from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.utils import timezone
from django.db.models import Prefetch, Sum, Avg, Q, Value, F
from django.db.models.functions import Coalesce
from decimal import Decimal
from django.shortcuts import get_object_or_404

from store.models import (
    StatusChoices,
    SliderType,
    VariantType,
    Category,
    Brand,
    Color,
    Size,
    Product,
    Gallery,
    VariantOption,
    Slider,
    Review,
    AllowPayment,
)

from store.serializers import (
    CategorySerializer,
    BrandSerializer,
    ColorSerializer,
    SizeSerializer,
    ProductSerializer,
    GallerySerializer,
    VariantOptionSerializer,
    SliderSerializer,
    ReviewSerializer,
    AllowPaymentSerializer
)

# ==============================================================================
# HELPER FUNCTIONS
# ==============================================================================

def get_product_variants(product, selected_size_id=None):
    """
    Fetches active variants, extracts unique sizes and colors, and handles selected variant logic.
    Optimized with `select_related` and converted to a list in memory to prevent N+1 query issues.
    """
    # Fetch all active variants and convert to list to avoid repeated database hits
    variants = list(
        product.variants.filter(status=StatusChoices.Active, stock__gt=0)
        .select_related('size', 'color')
    )

    # Return default empty structure if no variants are available
    if not variants:
        return {
            "sizes": [],
            "colors": [],
            "selected_variant": None,
            "all_variants": []
        }

    # Extract unique size options using a set for lookup
    sizes, seen_sizes = [], set()
    for v in variants:
        if v.size and v.size.id not in seen_sizes:
            sizes.append({'id': v.size.id, 'code': v.size.title})
            seen_sizes.add(v.size.id)

    # Resolve selected variant based on passed size_id or fallback to first item
    variant = None
    if selected_size_id:
        variant = next((v for v in variants if v.size and str(v.size.id) == str(selected_size_id)), None)
    
    if not variant:
        variant = variants[0]  # In-memory indexing (faster than .first())

    # Filter color choices based on target selected size
    target_size = variant.size if variant else None
    colors = [
        {
            "id": v.color.id, 
            "title": v.color.title, 
            "variant_id": v.id,
            "price": v.variant_price,
            "stock": v.stock
        }
        for v in variants 
        if v.color and (target_size is None or v.size == target_size)
    ]

    return {
        "sizes": sizes,
        "colors": colors,
        "selected_variant": {
            "id": variant.id,
            "price": variant.variant_price,
            "stock": variant.stock,
            "size": variant.size.title if variant.size else None,
            "color": variant.color.title if variant.color else None,
        } if variant else None,
        "all_variants": variants
    }


def success(message, data=None, code=200):
    """
    Standardized success API response wrapper.
    """
    return Response(
        {
            "success": True,
            "message": message,
            "data": data
        },
        status=code
    )


def error(message, code=400):
    """
    Standardized error API response wrapper.
    """
    return Response(
        {
            "success": False,
            "message": message
        },
        status=code
    )


# ==============================================================================
# API ROOT VIEW
# ==============================================================================
class APIRoot(APIView):
    """
    Provides an entry point listing all main store API endpoints.
    """
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        product = Product.objects.filter(status=StatusChoices.Active).select_related(
            "category", "brand"
        ).first()

        slug = product.slug if product else "example-product"
        product_id = product.id if product else 1

        return Response({
            "home": "http://127.0.0.1:8000/api/store/home/",
            "product_detail": f"http://127.0.0.1:8000/api/store/product/detail/{slug}/{product_id}/",
            "get_variant_by_size": "http://127.0.0.1:8000/api/store/get/variant/by/size/",
            "get_variant_by_color": "http://127.0.0.1:8000/api/store/get/variant/by/color/",
            "get_filter_products": "http://127.0.0.1:8000/api/store/get/filter/products/",
            "product_reviews": "http://127.0.0.1:8000/api/store/product/reviews/",
            "shopping": "http://127.0.0.1:8000/api/store/shopping/",
            "category_products": "http://127.0.0.1:8000/api/store/category/products/",
            "searching_products": "http://127.0.0.1:8000/api/store/searching/products/",
            "auto_search_complete": "http://127.0.0.1:8000/api/store/auto/search/complete/",
        })


# ==============================================================================
# HOME PAGE API VIEW
# ==============================================================================
class HomeViewAPI(APIView):
    """
    Fetches active sliders, payment gateways, featured products, deals, and active customer reviews.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        now = timezone.now()

        # Query active sliders and promotional banners
        sliders_qs = (
            Slider.objects
            .filter(status=StatusChoices.Active)
            .select_related("product")
        )

        # Query accepted payment methods
        allow_payment_qs = (
            AllowPayment.objects
            .filter(status=StatusChoices.Active)
        )

        # Base optimized queryset for active products
        products_qs = (
            Product.objects
            .filter(status=StatusChoices.Active)
            .annotate(
                total_variant_stock=Coalesce(
                    Sum("variants__stock", filter=Q(variants__status=StatusChoices.Active)), Value(0)
                ),
                avg_rate=Coalesce(
                    Avg("reviews__rating", filter=Q(reviews__status=StatusChoices.Active)), Value(Decimal("0.0"))
                )
            )
            .filter(Q(stock__gt=0) | Q(total_variant_stock__gt=0))
            .select_related("category", "brand")
            .prefetch_related(
                Prefetch(
                    "variants", 
                    queryset=VariantOption.objects.filter(status=StatusChoices.Active)
                    .select_related("size", "color").order_by("id")
                ),
                Prefetch(
                    "galleries", 
                    queryset=Gallery.objects.filter(status=StatusChoices.Active)
                ),
            )
        )

        # Fetch active reviews
        reviews_qs = (
            Review.objects
            .filter(status=StatusChoices.Active)
            .select_related("user")
            .order_by("-id")
        )
        
        data = {
            "sliders": SliderSerializer(
                sliders_qs.filter(slider_type=SliderType.SLIDER), many=True
            ).data,

            "adds": SliderSerializer(
                sliders_qs.filter(slider_type=SliderType.ADD), many=True
            ).data,

            "featured": SliderSerializer(
                sliders_qs.filter(slider_type=SliderType.FEATURE), many=True
            ).data,

            "promotions": SliderSerializer(
                sliders_qs.filter(slider_type=SliderType.PROMOTION), many=True
            ).data,

            "allow_payment": AllowPaymentSerializer(
                allow_payment_qs, many=True
            ).data,

            "featured_products": ProductSerializer(
                products_qs.filter(is_featured=True).order_by('-id')[:8], many=True
            ).data,
            
            "deal_products": ProductSerializer(
                products_qs
                .filter(discount__gt=0, is_deadline=True, deadline__gte=now)
                .order_by("-discount", "deadline")[:6], many=True
            ).data,

            "reviews": ReviewSerializer(
                reviews_qs, many=True
            ).data
        }

        return success(message="Home data fetched successfully.", data=data)


# ==============================================================================
# PRODUCT DETAIL API VIEW
# ==============================================================================
class ProductDetailViewAPI(APIView):
    """
    Fetches detailed product information, variant combinations, gallery images, 
    reviews, and related products based on category/brand.
    """
    permission_classes = [AllowAny]

    def get_object(self, slug, id):
        """
        Retrieves active product matching slug and ID with pre-fetched relations.
        """
        return get_object_or_404(
            Product.objects.filter(status=StatusChoices.Active)
            .annotate(
                total_variant_stock=Coalesce(
                    Sum("variants__stock", filter=Q(variants__status=StatusChoices.Active)), Value(0)
                ),
                avg_rate=Coalesce(
                    Avg("reviews__rating", filter=Q(reviews__status=StatusChoices.Active)), Value(Decimal("0.0"))
                )
            )
            .filter(Q(stock__gt=0) | Q(total_variant_stock__gt=0))
            .select_related("category", "brand")
            .prefetch_related(
                Prefetch(
                    "variants", 
                    queryset=VariantOption.objects.filter(status=StatusChoices.Active)
                    .select_related("size", "color").order_by("id")
                ),
                Prefetch(
                    "galleries", 
                    queryset=Gallery.objects.filter(status=StatusChoices.Active)
                ),
                Prefetch(
                    "reviews", 
                    queryset=Review.objects.filter(status=StatusChoices.Active).select_related("user")
                ),
            ),
            slug=slug,
            id=id
        )

    def get(self, request, slug, id):
        product = self.get_object(slug, id)
        
        # Increment visit counter atomically to prevent race conditions
        Product.objects.filter(id=product.id).update(visited=F('visited') + 1)
        
        # Query related products based on Category or Brand (Replaced order_by('?') for performance)
        related_products = (
            Product.objects
            .filter(status=StatusChoices.Active)
            .exclude(id=product.id)
            .filter(Q(category=product.category) | Q(brand=product.brand))
            .annotate(
                total_variant_stock=Coalesce(
                    Sum("variants__stock", filter=Q(variants__status=StatusChoices.Active)), Value(0)
                ),
                avg_rate=Coalesce(
                    Avg("reviews__rating", filter=Q(reviews__status=StatusChoices.Active)), Value(Decimal("0.0"))
                )
            )
            .filter(Q(stock__gt=0) | Q(total_variant_stock__gt=0))
            .select_related("category", "brand")
            .prefetch_related(
                Prefetch(
                    "variants", 
                    queryset=VariantOption.objects.filter(status=StatusChoices.Active)
                    .select_related("size", "color").order_by("id")
                ),
                Prefetch(
                    "galleries", 
                    queryset=Gallery.objects.filter(status=StatusChoices.Active)
                )
            )
            .order_by("-id")[:8]
        )

        # Process variant data if the product supports variants
        variant_data = None
        if product.variants_type != VariantType.NONE:
            selected_size_id = request.query_params.get('size')
            variant_data = get_product_variants(product, selected_size_id=selected_size_id)

        # Construct final structured API response payload
        data = {
            "product": ProductSerializer(product).data,
            "visited": product.visited + 1,
            "related_products": ProductSerializer(related_products, many=True).data,
            
            "variants": VariantOptionSerializer(
                variant_data["all_variants"] if variant_data else [], many=True
            ).data,

            "sizes": variant_data["sizes"] if variant_data else [],
            "colors": variant_data["colors"] if variant_data else [],
            "selected_variant": variant_data["selected_variant"] if variant_data else None,
                        
            "galleries": GallerySerializer(product.galleries.all(), many=True).data,
            "reviews": ReviewSerializer(product.reviews.all(), many=True).data,
        }

        return success(message="Product details fetched successfully.", data=data)


# ==============================================================================
# DRF API: FETCH COLOR VARIANTS BY SIZE
# ==============================================================================
class GetVariantBySizeViewAPI(APIView):
    """
    API endpoint to retrieve available color variants dynamically when a size is selected.
    Replaces template HTML rendering with structured JSON payload.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            # REST Framework handles both request.data (JSON) and Form Data
            product_id = request.data.get('product_id')
            size_id = request.data.get('size_id')

            # Validate payload parameters
            if not product_id or not size_id:
                return error(message="Invalid payload: missing product_id or size_id", code=400)

            # Query matching active variants with available stock
            variants = (
                VariantOption.objects
                .filter(
                    product_id=product_id,
                    size_id=size_id,
                    status=StatusChoices.Active,
                    stock__gt=0
                ).select_related('product', 'size', 'color').order_by('id')
            )

            if not variants.exists():
                return error(message="Variant not found", code=404)

            # Format available colors for frontend UI rendering
            colors_data = [
                {
                    "id": v.color.id if v.color else None,
                    "title": v.color.title if v.color else None,
                    "variant_id": v.id,
                    "price": v.variant_price,
                    "stock": v.stock,
                }
                for v in variants
            ]

            data = {
                "variant": VariantOptionSerializer(variants.first()).data,
                "colors": colors_data,
            }

            return success(message="Success Sizes", data=data)

        except Exception as e:
            return error(message="Unable to fetch variant", code=500)


# ==============================================================================
# DRF API: FETCH VARIANT BY COLOR
# ==============================================================================
class GetVariantByColorViewAPI(APIView):
    """
    API endpoint to fetch details of a specific variant option when selected.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            variant_id = request.data.get('variant_id')

            # Validate payload parameters
            if not variant_id:
                return error(message="Variant ID is required",  code=400)

            # Fetch active variant with positive stock
            variant = (
                VariantOption.objects
                .select_related('product', 'size', 'color')
                .filter(id=variant_id, status=StatusChoices.Active, stock__gt=0).first()
            )

            if not variant:
                return error(message="Please select a size before selecting a color", code=404 )

            data = {
                "variant_id": variant.id,
                "variant": VariantOptionSerializer(variant).data,
                "details": {
                    "id": variant.id,
                    "price": variant.variant_price,
                    "stock": variant.stock,
                    "size": variant.size.title if variant.size else None,
                    "color": variant.color.title if variant.color else None,
                }
            }

            return success(message="Success Colors", data=data)

        except Exception as e:
            return error(message="Unable to fetch variant", code=500)


# ======================== GET FILTER ===========================
class GetFilterProductsViewAPI(APIView):
    permission_classes = [AllowAny]
    def post(self, request):   
        try:
            products_qs = (
                Product.objects
                .filter(status=StatusChoices.Active)
                .annotate(
                    # Total active variant stock
                    total_variant_stock=Coalesce(
                        Sum(
                            "variants__stock", filter=Q(variants__status=StatusChoices.Active)
                        ), Value(0)),

                    # Average active review rating
                    avg_rate=Coalesce(
                        Avg(
                            "reviews__rating", filter=Q(reviews__status=StatusChoices.Active)
                        ), Value(Decimal("0.0")),
                    )
                )
                .filter(Q(stock__gt=0) | Q(total_variant_stock__gt=0)).select_related("category", "brand")
                .prefetch_related(
                    # Active variants
                    Prefetch(
                        "variants", queryset=(
                            VariantOption.objects.filter(status=StatusChoices.Active)
                            .select_related("size", "color").order_by("id")
                        )
                    ),
                    # Active galleries
                    Prefetch(
                        "galleries", queryset=Gallery.objects.filter(status=StatusChoices.Active),
                    ),
                )
            )

            category_ids = request.data.get("category", [])
            if category_ids:
                products_qs = products_qs.filter(
                    category_id__in=category_ids
                )

            brand_ids = request.data.get("brand", [])
            if brand_ids:
                products_qs = products_qs.filter(
                    brand_id__in=brand_ids
                )

            max_price = request.data.get("maxPrice")

            if max_price:
                products_qs = products_qs.filter(
                    sale_price__lte=Decimal(max_price)
                )

            serializer = ProductSerializer(
                products_qs,
                many=True
            )

            return Response(serializer.data)
        
        except Exception as e:
            return error(message="Unable to fetch variant", code=500)


# =============================== SHOP LIST =========================
class ShopViewAPI(APIView):
    permission_classes = [AllowAny]
    def get(self, request):

        products_qs = (
            Product.objects
            .filter(status=StatusChoices.Active)
            .annotate(
                # Total active variant stock
                total_variant_stock=Coalesce(
                    Sum(
                        "variants__stock", filter=Q(variants__status=StatusChoices.Active)
                    ), Value(0)),

                # Average active review rating
                avg_rate=Coalesce(
                    Avg(
                        "reviews__rating", filter=Q(reviews__status=StatusChoices.Active)
                    ), Value(Decimal("0.0")),
                )
            )
            .filter(Q(stock__gt=0) | Q(total_variant_stock__gt=0)).select_related("category", "brand")
            .prefetch_related(
                # Active variants
                Prefetch(
                    "variants", queryset=(
                        VariantOption.objects.filter(status=StatusChoices.Active)
                        .select_related("size", "color").order_by("id")
                    )
                ),
                # Active galleries
                Prefetch(
                    "galleries", queryset=Gallery.objects.filter(status=StatusChoices.Active),
                ),
            )
        )

        banners = Slider.objects.filter(
            slider_type=SliderType.ADD,
            status=StatusChoices.Active
        )[:1]

        try:
            per_page = int(
                request.GET.get("per_page") or 3
            )

            page_number = int(
                request.GET.get("page") or 1
            )

        except ValueError:
            per_page = 3
            page_number = 1


        sort_by = request.GET.get(
            "sort",
            "latest"
        )

        if sort_by == "upcoming":

            products_qs = (
                products_qs
                .filter(
                    deadline__gt=timezone.now()
                )
                .order_by(
                    "deadline"
                )
            )

        else:

            sort_map = {
                "latest": "-created_at",
                "new": "created_at",
            }

            products_qs = (
                products_qs
                .order_by(
                    sort_map.get(
                        sort_by,
                        "-created_at"
                    )
                )
            )


        paginator = Paginator(
            products_qs,
            per_page
        )

        page_obj = paginator.get_page(
            page_number
        )

        data = {
            "banners": SliderSerializer(
                banners,
                many=True
            ).data,

            "products": ProductSerializer(
                page_obj.object_list,
                many=True
            ).data,

            "pagination": {
                "current_page": page_obj.number,
                "total_pages": paginator.num_pages,
                "total_items": paginator.count,
                "has_next": page_obj.has_next(),
                "has_previous": page_obj.has_previous(),
            }
        }

        return success(
            message="Shop data fetched successfully.",
            data=data
        )


# =============================== CATEGORY PRODUCT ==========================
class CategoryProductViewAPI(APIView):
    permission_classes = [AllowAny]

    def get(self, request, slug, id):

        category = get_object_or_404(
            Category,
            slug=slug,
            id=id,
            status=StatusChoices.Active
        )

        products_qs = (
            Product.objects
            .filter(status=StatusChoices.Active)
            .annotate(
                # Total active variant stock
                total_variant_stock=Coalesce(
                    Sum(
                        "variants__stock", filter=Q(variants__status=StatusChoices.Active)
                    ), Value(0)),

                # Average active review rating
                avg_rate=Coalesce(
                    Avg(
                        "reviews__rating", filter=Q(reviews__status=StatusChoices.Active)
                    ), Value(Decimal("0.0")),
                )
            )
            .filter(Q(stock__gt=0) | Q(total_variant_stock__gt=0)).select_related("category", "brand")
            .prefetch_related(
                # Active variants
                Prefetch(
                    "variants", queryset=(
                        VariantOption.objects.filter(status=StatusChoices.Active)
                        .select_related("size", "color").order_by("id")
                    )
                ),
                # Active galleries
                Prefetch(
                    "galleries", queryset=Gallery.objects.filter(status=StatusChoices.Active),
                ),
            )
        )

        sort_by = request.GET.get(
            "sort",
            "latest"
        )


        if sort_by == "upcoming":

            products_qs = (
                products_qs
                .filter(
                    deadline__gt=timezone.now()
                )
                .order_by(
                    "deadline"
                )
            )

        elif sort_by == "new":

            products_qs = (
                products_qs
                .order_by(
                    "created_at"
                )
            )

        else:

            products_qs = (
                products_qs
                .order_by(
                    "-created_at"
                )
            )


        per_page_options = [
            3,
            6,
            12,
            24
        ]


        try:

            per_page = int(
                request.GET.get(
                    "per_page",
                    3
                )
            )

        except ValueError:

            per_page = 3


        if per_page not in per_page_options:

            per_page = 3


        paginator = Paginator(
            products_qs,
            per_page
        )


        page_obj = paginator.get_page(
            request.GET.get(
                "page",
                1
            )
        )


        banners = (
            Slider.objects
            .filter(
                slider_type=SliderType.ADD,
                status=StatusChoices.Active
            )[:1]
        )


        data = {

            "category": CategorySerializer(
                category
            ).data,

            "banners": SliderSerializer(
                banners,
                many=True
            ).data,

            "products": ProductSerializer(
                page_obj.object_list,
                many=True
            ).data,

            "pagination": {
                "current_page": page_obj.number,
                "total_pages": paginator.num_pages,
                "total_items": paginator.count,
                "has_next": page_obj.has_next(),
                "has_previous": page_obj.has_previous(),
            }
        }


        return success(
            message="Category products fetched successfully.",
            data=data
        )


# ========================= REVIEW ===============================
class ProductReviewViewAPI(APIView):

    def post(self, request):

        serializer = ReviewSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user)

            return Response({
                    "success": True,
                    "message": "Review submitted",
                    "data": serializer.data
                },
                status=status.HTTP_201_CREATED)

        return Response({
                "success": False,
                "errors": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST)


# ============================= SEARCH ===============================
class SearchingViewAPI(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        query = request.data.get('q', '').strip()

        products_qs = (
            Product.objects
            .filter(status=StatusChoices.Active)
            .annotate(
                # Total active variant stock
                total_variant_stock=Coalesce(
                    Sum(
                        "variants__stock", filter=Q(variants__status=StatusChoices.Active)
                    ), Value(0)),

                # Average active review rating
                avg_rate=Coalesce(
                    Avg(
                        "reviews__rating", filter=Q(reviews__status=StatusChoices.Active)
                    ), Value(Decimal("0.0")),
                )
            )
            .filter(Q(stock__gt=0) | Q(total_variant_stock__gt=0)).select_related("category", "brand")
            .prefetch_related(
                # Active variants
                Prefetch(
                    "variants", queryset=(
                        VariantOption.objects.filter(status=StatusChoices.Active)
                        .select_related("size", "color").order_by("id")
                    )
                ),
                # Active galleries
                Prefetch(
                    "galleries", queryset=Gallery.objects.filter(status=StatusChoices.Active),
                ),
            )
        )

        # Search filter
        if query:
            products_qs = products_qs.filter(
                Q(title__icontains=query) |
                Q(slug__icontains=query) |
                Q(category__title__icontains=query) |
                Q(brand__title__icontains=query)
            ).distinct()

        data = ProductSerializer(
            products_qs,
            many=True,
            context={"request": request}
        ).data

        return Response({
            "success": True,
            "count": len(data),
            "results": data
        })


# ====================== AUTO COMPLETE ==========================
class AutoSearchCompleteAPI(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        term = request.GET.get("term", "").strip()
        results = []

        products_qs = (
            Product.objects
            .filter(status=StatusChoices.Active)
            .annotate(
                # Total active variant stock
                total_variant_stock=Coalesce(
                    Sum(
                        "variants__stock", filter=Q(variants__status=StatusChoices.Active)
                    ), Value(0)),

                # Average active review rating
                avg_rate=Coalesce(
                    Avg(
                        "reviews__rating", filter=Q(reviews__status=StatusChoices.Active)
                    ), Value(Decimal("0.0")),
                )
            )
            .filter(Q(stock__gt=0) | Q(total_variant_stock__gt=0)).select_related("category", "brand")
            .prefetch_related(
                # Active variants
                Prefetch(
                    "variants", queryset=(
                        VariantOption.objects.filter(status=StatusChoices.Active)
                        .select_related("size", "color").order_by("id")
                    )
                ),
                # Active galleries
                Prefetch(
                    "galleries", queryset=Gallery.objects.filter(status=StatusChoices.Active),
                ),
            )
        )

        if term:
            products_qs = (
                products_qs
                .filter(
                    Q(title__icontains=term)
                )
                .distinct()[:6]
            )

            for product in products_qs:
                results.append({
                    "id": product.id,
                    "label": product.title,
                    "value": product.title,
                    "slug": product.slug,
                    "avg_rate": product.avg_rate,
                })

        return Response(results)





