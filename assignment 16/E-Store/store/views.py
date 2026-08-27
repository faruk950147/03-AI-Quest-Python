from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.contrib import messages
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.db.models import Prefetch, Avg, Q, Sum, Value, F
from decimal import Decimal, InvalidOperation
from django.db.models.functions import Coalesce
from django.template.loader import render_to_string
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator
import logging

# import from local
from mixins.mixing import LoginRequiredMixin
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
from store.forms import ReviewForm

logger = logging.getLogger(__name__)


# ==============================================================================
# VARIANTS HELPER FUNCTION
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
        return {"sizes": [], "colors": [], "selected_variant": None, "all_variants": []}

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
    colors = [{
        "id": v.color.id, 
        "title": v.color.title, 
        "variant_id": v.id,
        "price": v.variant_price,
        "stock": v.stock}
        for v in variants if v.color and (target_size is None or v.size == target_size)
    ]

    return {
        "sizes": sizes,
        "colors": colors,
        "selected_variant": {
            "id": variant.id,
            "price": variant.variant_price,
            "stock": variant.stock,
            "sku": variant.sku,
            "size": variant.size.title if variant.size else None,
            "color": variant.color.title if variant.color else None,
        } if variant else None,
        "all_variants": variants
    }


# ==============================================================================
# HOME PAGE VIEW
# ==============================================================================
@method_decorator(never_cache, name="dispatch")
class HomeView(View):
    """
    Renders the e-commerce home page featuring active sliders, 
    featured products, deals, and customer reviews.
    """

    def get(self, request):
        now = timezone.now()

        # Query active homepage hero sliders and featured banners
        sliders_qs = (
            Slider.objects
            .filter(status=StatusChoices.Active)
            .select_related("product")
        )

        # Query supported payment gateways
        allow_payment_qs = (
            AllowPayment.objects
            .filter(status=StatusChoices.Active)
        )

        # Base QuerySet for active products with aggregated total stock and rating average
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

        # Query latest approved product reviews
        reviews_qs = (
            Review.objects
            .filter(status=StatusChoices.Active)
            .select_related("user")
            .order_by("-id")
        )
        
        context = {
            "sliders": sliders_qs.filter(slider_type=SliderType.SLIDER),
            "featured": sliders_qs.filter(slider_type=SliderType.FEATURE),
            "allow_payments": allow_payment_qs,
            "featured_products": products_qs.filter(is_featured=True).order_by('-id')[:8],
            "deal_products": (
                products_qs
                .filter(discount__gt=0, is_deadline=True, deadline__gte=now)
                .order_by("-discount", "deadline")[:6]
            ),
            "reviews": reviews_qs
        }

        logger.info("Home page accessed by user: %s", request.user.username)
        return render(request, "store/home.html", context)


# ==============================================================================
# PRODUCT DETAIL VIEW
# ==============================================================================
@method_decorator(never_cache, name='dispatch')
class ProductView(View):
    """
    Renders detailed information for a single product, including variant attributes,
    gallery images, active reviews, and related category/brand products.
    """

    def get_object(self, slug, id):
        """
        Retrieves active product matching slug/id, pre-fetching variants, gallery, and reviews.
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

        # Atomic counter increment to avoid race conditions when tracking page visits
        Product.objects.filter(id=product.id).update(visited=F('visited') + 1)
        
        # Query related products matching category or brand (Optimized ordering over random)
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
                    queryset=VariantOption.objects.filter(status=StatusChoices.Active).select_related("size", "color").order_by("id")
                ),
                Prefetch(
                    "galleries", 
                    queryset=Gallery.objects.filter(status=StatusChoices.Active)
                )
            )
            .order_by("-id")[:8]  # Replaced order_by('?') for high query performance
        )

        # Process variant options if the product supports variants
        variant_data = None
        if product.variants_type != VariantType.NONE:
            selected_size_id = request.GET.get('size')
            variant_data = get_product_variants(product, selected_size_id=selected_size_id)
            
        context = {
            'product': product,
            'variant_data': variant_data,
            'related_products': related_products,
            'form': ReviewForm
        }
        logger.info(f"Product page accessed by user: {request.user.username}")
        return render(request, 'store/product-detail.html', context)


# ==============================================================================
# AJAX VIEW: FETCH COLOR VARIANTS BY SIZE
# ==============================================================================
@method_decorator(never_cache, name="dispatch")
class GetVariantBySizeView(View):
    """
    AJAX endpoint to retrieve and render available color options
    dynamically when a size is selected.
    """

    def post(self, request):
        try:
            product_id = request.POST.get("product_id")
            size_id = request.POST.get("size_id")

            # Validate payload
            if not product_id or not size_id:
                return JsonResponse({
                        "error": "Invalid payload: missing product_id or size_id"
                    }, status=400)



            # Get all matching active variants with stock
            variants = list(
                VariantOption.objects.filter(
                    product_id=product_id,
                    size_id=size_id,
                    status=StatusChoices.Active,
                    stock__gt=0,
                )
                .select_related("product", "size", "color").order_by("id")
            )

            # No available variant
            if not variants:
                return JsonResponse({"error": "Variant not found"}, status=404)

            # Render all available colors
            html = render_to_string(
                "store/components/variant_options.html", {"colors": variants},
                request=request,
            )

            # First variant for default variant information
            variant = variants[0]

            return JsonResponse({
                    "rendered_colors": html,
                    "variant_id": variant.id,
                    "variant_price": str(variant.variant_price),
                    "variant_image": variant.image_url,
                    "available_stock": variant.stock,

                    "size": (
                        variant.size.code
                        if variant.size
                        else ""
                    ),

                    "color": (
                        variant.color.title
                        if variant.color
                        else ""
                    ),

                    "sku": variant.sku,

                    "message": "Success Sizes",
                })

        except Exception as e:
            return JsonResponse(
                {"error": "Something went wrong", "detail": str(e)},
                status=500,
            )


# ==============================================================================
# AJAX VIEW: FETCH VARIANT BY COLOR
# ==============================================================================
@method_decorator(never_cache, name="dispatch")
class GetVariantByColorView(View):
    """
    AJAX endpoint to fetch details of a specific variant
    when a color is selected.
    """

    def post(self, request):
        try:
            variant_id = request.POST.get("variant_id")

            # Validate payload
            if not variant_id:
                return JsonResponse({"error": "Variant ID is required"}, status=400)

            # Fetch active variant with available stock
            variant = (
                VariantOption.objects
                .select_related("product", "size", "color")
                .filter(id=variant_id, status=StatusChoices.Active, stock__gt=0).first()
            )

            if not variant:
                return JsonResponse({"error": "Variant not found or out of stock"},status=404)

            return JsonResponse({
                    "variant_id": variant.id,
                    "variant_price": str(variant.variant_price),
                    "variant_image": variant.image_url,
                    "available_stock": variant.stock,
                    "size": (
                        variant.size.code
                        if variant.size
                        else ""
                    ),
                    "color": (
                        variant.color.title
                        if variant.color
                        else ""
                    ),
                    "sku": variant.sku,
                    "message": "Success Colors",
                })

        except Exception as e:
            return JsonResponse({
                "error": "Something went wrong", "detail": str(e)},
                status=500,
            )


# ======================== GET FILTER ===========================
class GetFilterProductsView(View):
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
            
            category_ids = request.POST.getlist('category[]')
            if category_ids:
                products_qs = products_qs.filter(category_id__in=category_ids)

            brand_ids = request.POST.getlist('brand[]')
            if brand_ids:
                products_qs = products_qs.filter(brand_id__in=brand_ids)

            max_price = request.POST.get('maxPrice')
            if max_price:
                try:
                    max_price = Decimal(max_price)
                    products_qs = products_qs.filter(sale_price__lte=max_price)
                except:
                    pass

            html = render_to_string('store/components/grid.html', {'products_qs': products_qs}, request=request)
            return JsonResponse({'html': html})
        
        except Exception as e:
            logger.error(f"GetFilterProductsView error: {e}", exc_info=True)
            return JsonResponse({'html':'<p>Error loading products</p>'})


# =============================== SHOP LIST =========================
class ShopView(View):

    def get(self, request):
        try:
            per_page_options = [3, 6, 12]
            sort_options = ['latest', 'new', 'upcoming']
            
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
            
            # Pagination parameters
            try:
                per_page = int(request.GET.get("per_page") or 3)
                page_number = int(request.GET.get("page") or 1)
                
            except (ValueError, TypeError):
                per_page = 3
                page_number = 1

            # Validate per_page
            if per_page not in per_page_options:
                per_page = 3

            # Sorting
            sort_by = request.GET.get("sort", "latest")

            if sort_by == "upcoming":
                products = (products_qs.filter(deadline__gt=timezone.now())
                    .order_by("deadline")
                )

            else:
                sort_map = {"latest": "-created_at", "new": "created_at"}

                products = products_qs.order_by(sort_map.get(sort_by, "-created_at"))

            # Pagination
            paginator = Paginator(products, per_page)

            page_obj = paginator.get_page(page_number)

            context = {
                "products_qs": page_obj,
                "page_obj": page_obj,
                "per_page_options": per_page_options,
                "sort_options": sort_options,
                "selected_per_page": per_page,
                "selected_sort": sort_by,
            }

            # AJAX Request
            if request.headers.get("x-requested-with") == "XMLHttpRequest":

                return JsonResponse({
                    "html": render_to_string("store/components/grid.html", context, request=request),
                    "pagination_html": render_to_string(
                        "store/components/pagination.html", context, request=request
                    )
                })

            return render(request, "store/shopping.html", context)

        except Exception as e:
            logger.error(f"ShopView error: {e}", exc_info=True)

            return render(request,"store/shopping.html", {"products": [], "page_obj": None})        


# =============================== CATEGORY PRODUCT ==========================
class CategoryProductView(View):
    def get(self, request, slug, id):
        try:
            category = get_object_or_404(Category, slug=slug, id=id)
            per_page_options = [3, 6, 12]
            sort_options = ['latest', 'new', 'upcoming']
            
            products_qs = (
                Product.objects
                .filter(category=category, status=StatusChoices.Active)
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
            
            # Pagination parameters
            try:
                per_page = int(request.GET.get("per_page") or 3)
                page_number = int(request.GET.get("page") or 1)
                
            except (ValueError, TypeError):
                per_page = 3
                page_number = 1

            # Validate per_page
            if per_page not in per_page_options:
                per_page = 3

            # Sorting
            sort_by = request.GET.get("sort", "latest")

            if sort_by == "upcoming":
                products = (products_qs.filter(deadline__gt=timezone.now())
                    .order_by("deadline")
                )

            else:
                sort_map = {"latest": "-created_at", "new": "created_at"}

                products = products_qs.order_by(sort_map.get(sort_by, "-created_at"))

            # Pagination
            paginator = Paginator(products, per_page)

            page_obj = paginator.get_page(page_number)

            context = {
                "products_qs": page_obj,
                "page_obj": page_obj,
                "per_page_options": per_page_options,
                "sort_options": sort_options,
                "selected_per_page": per_page,
                "selected_sort": sort_by,
            }

            # AJAX Request
            if request.headers.get("x-requested-with") == "XMLHttpRequest":

                return JsonResponse({
                    "html": render_to_string("store/components/grid.html", context, request=request),
                    "pagination_html": render_to_string(
                        "store/components/pagination.html", context, request=request
                    )
                })

            return render(request, "store/shopping.html", context)

        except Exception as e:
            logger.error(f"ShopView error: {e}", exc_info=True)

            return render(request,"store/shopping.html", {"products": [], "page_obj": None})        


# ========================= REVIEW =========================
@method_decorator(never_cache, name='dispatch')
class ProductReviewView(LoginRequiredMixin, View):
    def post(self, request):
        try:
            user = request.user
            product_slug = request.POST.get('product_slug')
            product_id = request.POST.get('product_id')
            rating = request.POST.get('rating')
            subject = request.POST.get('subject')
            comment = request.POST.get('comment')

            if not product_slug or not product_id:
                return JsonResponse({
                    'status': 'error', 'message': 'Product information is missing.'
                }, status=400)

            if not rating:
                return JsonResponse({
                    'status': 'error', 'message': 'Please select a rating.'
                }, status=400)

            if not subject or not subject.strip():
                return JsonResponse({
                    'status': 'error', 'message': 'Please enter a subject.'
                }, status=400)

            if not comment or not comment.strip():
                return JsonResponse({
                    'status': 'error', 'message': 'Please enter a comment.'
                }, status=400)

            try:
                rating = Decimal(rating)
            except (InvalidOperation, TypeError, ValueError):
                return JsonResponse({'status': 'error', 'message': 'Please select a valid rating.'}, status=400)

            if not Decimal('1.0') <= rating <= Decimal('5.0'):
                return JsonResponse({
                    'status': 'error', 'message': 'Rating must be between 1 and 5.'
                }, status=400)


            product = get_object_or_404(
                Product.objects.filter(Q(stock__gt=0) | Q(variants__stock__gt=0)).distinct(),
                id=product_id,
                slug=product_slug,
                status=StatusChoices.Active,
            )

            if Review.objects.filter(user=user, product=product, status=StatusChoices.Active,).exists():
                return JsonResponse({
                    'status': 'error', 'message': 'You have already reviewed this product.'
                }, status=400)


            review = Review.objects.create(
                user=user,
                product=product,
                rating=rating,
                subject=subject.strip(),
                comment=comment.strip(),
            )

            review_count = product.reviews.filter(
                status=StatusChoices.Active
            ).count()

            review_html = render_to_string(
                'store/components/review_item.html', {'review': review, 'user': user},
                request=request,
            )

            return JsonResponse({
                'status': 'success',
                'message': 'Review submitted successfully.',
                'review_count': review_count,
                'review_html': review_html,
            })

        except Exception as e:
            logger.error(f'ProductReviewView error: {e}', exc_info=True)

            return JsonResponse({
                'status': 'error', 'message': 'Unable to submit review.'
            }, status=500)


# ============================= SEARCH ===============================
class SearchingView(View):
    def post(self, request):
        query = request.POST.get("q", "").strip()

        products_qs = (
            Product.objects
            .filter(status=StatusChoices.Active)
            .annotate(
                # Total active variant stock
                total_variant_stock=Coalesce(
                    Sum("variants__stock", filter=Q(variants__status=StatusChoices.Active),), Value(0),
                ),

                # Average active review rating
                avg_rate=Coalesce(
                    Avg("reviews__rating", filter=Q(reviews__status=StatusChoices.Active),), Value(Decimal("0.0")),
                )
            )
            .filter(Q(stock__gt=0) | Q(total_variant_stock__gt=0)).select_related("category", "brand",)
            .prefetch_related(
                # Active variants
                Prefetch(
                    "variants",
                    queryset=(VariantOption.objects.filter(status=StatusChoices.Active)
                    .select_related("size", "color")
                    .order_by("id")),
                ),

                # Active galleries
                Prefetch(
                    "galleries",
                    queryset=(Gallery.objects.filter(status=StatusChoices.Active).order_by("id")),
                ),
            )
        )

        # Search filter
        if query:
            products_qs = (
                products_qs.filter(
                    Q(title__icontains=query) |
                    Q(slug__icontains=query) |
                    Q(category__title__icontains=query) |
                    Q(brand__title__icontains=query)
                ).distinct()
            )

        context = {
            "products_qs": products_qs,
            "query": query,
        }

        return render(request, "store/search.html", context)
    
    
# ====================== AUTO COMPLETE ==========================
@method_decorator(never_cache, name='dispatch')
class AutoSearchComplete(View):
    def get(self, request):
        term = request.GET.get("term", "").strip()

        results = []

        if not term:
            return JsonResponse(results, safe=False)

        products_qs = (
            Product.objects
            .filter(status=StatusChoices.Active)
            .annotate(
                # Total active variant stock
                total_variant_stock=Coalesce(
                    Sum("variants__stock", filter=Q(variants__status=StatusChoices.Active),), Value(0),
                ),

                # Average active review rating
                avg_rate=Coalesce(
                    Avg("reviews__rating", filter=Q(reviews__status=StatusChoices.Active),), Value(Decimal("0.0")),
                )
            )
            .filter(Q(stock__gt=0) | Q(total_variant_stock__gt=0)).select_related("category", "brand",)
            .prefetch_related(
                # Active variants
                Prefetch(
                    "variants",
                    queryset=(VariantOption.objects.filter(status=StatusChoices.Active)
                    .select_related("size", "color")
                    .order_by("id")),
                ),

                # Active galleries
                Prefetch(
                    "galleries",
                    queryset=(Gallery.objects.filter(status=StatusChoices.Active).order_by("id")),
                ),
            )
        )

        products = (
            products_qs.filter(title__icontains=term).distinct()[:6]
        )

        for product in products:
            gallery = product.galleries.first()

            results.append({
                "title": product.title,
                "price": f"{product.sale_price:.2f}",
                "image": gallery.image.url if gallery else "",
                "url": f"/product/{product.slug}/{product.id}/",
            })

        return JsonResponse(results, safe=False)



        
        
        
