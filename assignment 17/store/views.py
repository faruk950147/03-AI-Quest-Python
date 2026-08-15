from datetime import timedelta
from decimal import Decimal
import logging

from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.db.models import Avg, Q, Sum, F, Max, Min
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.utils import timezone
from datetime import timedelta
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

from account.mixing import LoginRequiredMixin
from store.models import (
    Product, ProductVariant, ImageGallery, Slider, Review,
    AcceptancePayment, Category, Brand
)

logger = logging.getLogger('project')

def get_product_variants(product):
    """
    Given a product, returns a dictionary containing:
    - first active variant
    - unique sizes
    - colors available for the first variant's size (if any)
    """
    variants = ProductVariant.objects.filter(
        product=product,
        status='active',
        available_stock__gt=0
    ).select_related('size', 'color').order_by('id')

    if not variants:
        return {'sizes': [], 'colors': [], 'variant': None}

    # Get the first active variant
    variant = variants[0]

    # Collect unique sizes
    sizes, seen_sizes = [], set()
    for v in variants:
        if v.size and v.size.id not in seen_sizes:
            sizes.append({'id': v.size.id, 'code': v.size.title})
            seen_sizes.add(v.size.id)

    # Get colors for the selected variant
    if variant.size:
        colors = [v for v in variants if v.size == variant.size]
    else:
        colors = [v for v in variants if v.color]

    return {'sizes': sizes, 'colors': colors, 'variant': variant}


# =========================================================
# HOME VIEW
# =========================================================
@method_decorator(never_cache, name='dispatch')
class HomeView(generic.View):
    def get(self, request):
        try:
            logger.info("Home page request started")

            # Sliders
            sliders_qs = Slider.objects.filter(status='active')
            sliders_dict = {
                'sliders': sliders_qs.filter(slider_type='slider'),
                'feature_sliders': sliders_qs.filter(slider_type='feature')[:4],
                'add_sliders': sliders_qs.filter(slider_type='add')[:2],
                'promo_sliders': sliders_qs.filter(slider_type='promotion')[:3],
            }

            # Acceptance payments
            acceptance_payments = AcceptancePayment.objects.filter(status='active')[:4]

            # Products
            products = Product.objects.filter(status='active').annotate(
                total_variant_stock=Sum('variants__available_stock', filter=Q(variants__status='active')),
                avg_rate=Avg('reviews__rating', filter=Q(reviews__status='active'))
            ).filter(Q(available_stock__gt=0) | Q(total_variant_stock__gt=0)) \
             .select_related('category', 'brand') \
             .prefetch_related('variants', 'variants__color', 'variants__size')

            # Top deals
            top_deals = products.filter(discount_percent__gt=0, is_deadline=True, deadline__gte=timezone.now()).order_by('-discount_percent', 'deadline')[:6]
            first_top_deal = top_deals[0] if top_deals else None

            # Featured
            featured_products = products.filter(is_featured=True)[:5]

            # Top sales
            top_sales_products = products.filter(sold__gt=0).order_by('-sold')[:6]

            # Recommendation / most visited
            recommendation_products = products.filter(Q(sold__gt=0) | Q(visited__gt=0)).order_by('-visited')[:8]

            # Trending last 7 days
            now = timezone.now()
            last_30_days = now - timedelta(days=30)

            trending_products = products.filter(
                sold__gt=0,
                visited__gt=0,
                created_at__gte=last_30_days
            ).order_by('-visited', '-sold')[:8]
            
            context = {
                **sliders_dict,
                'acceptance_payments': acceptance_payments,
                'top_deals': top_deals,
                'first_top_deal': first_top_deal,
                'featured_products': featured_products,
                'top_sales_products': top_sales_products,
                'recommendation_products': recommendation_products,
                'trending_products': trending_products
            }

            return render(request, 'store/home.html', context)

        except Exception as e:
            logger.error(f"HomeView GET error: {e}", exc_info=True)
            return render(request, 'store/home.html', {})


# =========================================================
# PRODUCT DETAIL VIEW
# =========================================================
@method_decorator(never_cache, name='dispatch')
class ProductDetailView(generic.View):
    def get(self, request, slug, id):
        try:
            product = get_object_or_404(
                Product.objects.select_related('category', 'brand')
                .annotate(avg_rate=Avg('reviews__rating', filter=Q(reviews__status='active'))),
                slug=slug,
                id=id,
                status='active',
                available_stock__gt=0
            )

            # Visit count
            session_key = f'viewed_product_{product.id}'
            if not request.session.get(session_key):
                Product.objects.filter(id=product.id).update(visited=F('visited') + 1)
                request.session[session_key] = True
                product.refresh_from_db()

            # Related products
            related_products = Product.objects.filter(
                category=product.category,
                status='active',
            ).exclude(id=product.id).order_by('-visited')[:4]

            context = {'product': product, 'related_products': related_products, 'sizes': [], 'colors': [], 'variant': None}

            # Variant logic
            if product.variant != 'none':
                # context.update(get_product_variants(product))
                
                variants = ProductVariant.objects.filter(
                    product=product,
                    status='active',
                    available_stock__gt=0
                ).select_related('size', 'color').order_by('id')

                if variants.exists():
                    variant = variants[0]
                    sizes, seen_sizes = [], set()
                    for v in variants:
                        if v.size and v.size.id not in seen_sizes:
                            sizes.append({'id': v.size.id, 'code': v.size.title})
                            seen_sizes.add(v.size.id)
                    if variant.size:
                        colors = [v for v in variants if v.size == variant.size]
                    else:
                        colors = [v for v in variants if v.color]

                    context.update({'sizes': sizes, 'colors': colors, 'variant': variant})

            return render(request, 'store/product-detail.html', context)

        except Exception as e:
            logger.error(f"ProductDetailView GET error: {e}", exc_info=True)
            return render(request, 'store/product-detail.html', {'product': None, 'related_products': [], 'sizes': [], 'colors': [], 'variant': None})


# =========================================================
# AJAX: Get Variant by Size
# =========================================================
@method_decorator(never_cache, name='dispatch')
class GetVariantBySizeView(generic.View):
    def post(self, request):
        try:
            product_id = request.POST.get('product_id')
            size_id = request.POST.get('size_id')

            variants_qs = ProductVariant.objects.filter(
                product_id=product_id, size_id=size_id,
                status='active', available_stock__gt=0
            ).select_related('size', 'color').order_by('id')

            variant = variants_qs.first()
            if not variant:
                return JsonResponse({'error': 'Variant not found'}, status=404)

            html = render_to_string('store/components/color_options.html', {'colors': variants_qs, 'variant': variant}, request=request)
            return JsonResponse({
                'rendered_colors': html,
                'variant_id': variant.id,
                'variant_price': str(variant.variant_price),
                'variant_image': variant.image_url,
                'available_stock': variant.available_stock,
                'size': variant.size.code if variant.size else '',
                'color': variant.color.title if variant.color else '',
                'sku': variant.sku,
            })

        except Exception as e:
            logger.error(f"GetVariantBySizeView error: {e}", exc_info=True)
            return JsonResponse({'error':'Unable to fetch variant'}, status=500)


# =========================================================
# AJAX: Get Variant by Color
# =========================================================
@method_decorator(never_cache, name='dispatch')
class GetVariantByColorView(generic.View):
    def post(self, request):
        try:
            variant_id = request.POST.get('variant_id')
            variant = ProductVariant.objects.select_related('size','color').filter(
                id=variant_id, status='active', available_stock__gt=0
            ).first()

            if not variant:
                return JsonResponse({'error':'Variant not found'}, status=404)

            return JsonResponse({
                'variant_id': variant.id,
                'variant_price': str(variant.variant_price),
                'available_stock': variant.available_stock,
                'variant_image': variant.image_url,
                'size': variant.size.code if variant.size else '',
                'color': variant.color.title if variant.color else '',
                'sku': variant.sku or '',
            })

        except Exception as e:
            logger.error(f"GetVariantByColorView error: {e}", exc_info=True)
            return JsonResponse({'error':'Unable to fetch variant'}, status=500)


# =========================================================
# AJAX: Filter Products
# =========================================================
@method_decorator(never_cache, name='dispatch')
class GetFilterProductsView(generic.View):
    def post(self, request):
        try:
            products_qs = Product.objects.filter(status='active').annotate(
                total_variant_stock=Sum('variants__available_stock', filter=Q(variants__status='active')),
                avg_rate=Avg('reviews__rating', filter=Q(reviews__status='active'))
            ).filter(Q(available_stock__gt=0) | Q(total_variant_stock__gt=0)) \
             .select_related('category','brand')

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

            html = render_to_string('store/components/grid.html', {'products': products_qs}, request=request)
            return JsonResponse({'html': html})

        except Exception as e:
            logger.error(f"GetFilterProductsView error: {e}", exc_info=True)
            return JsonResponse({'html':'<p>Error loading products</p>'})


# =========================================================
# AJAX: Product Review
# =========================================================
@method_decorator(never_cache, name='dispatch')
class ProductReviewView(LoginRequiredMixin, generic.View):
    def post(self, request):
        try:
            user = request.user
            product_slug = request.POST.get('product_slug')
            product_id = request.POST.get('product_id')
            rating = request.POST.get('rating')
            subject = request.POST.get('subject')
            comment = request.POST.get('comment')

            try: rating = float(rating)
            except: return JsonResponse({'status':'error','message':'Rating must be a number'})

            if not subject or not comment:
                return JsonResponse({'status':'error','message':'All fields are required'})
            if rating < 1 or rating > 5:
                return JsonResponse({'status':'error','message':'Rating must be between 1 and 5'})

            product = get_object_or_404(Product, slug=product_slug, id=product_id, status='active', available_stock__gt=0)

            if Review.objects.filter(user=user, product=product, status='active').exists():
                return JsonResponse({'status':'error','message':'You have already reviewed this product'})

            review = Review.objects.create(user=user, product=product, rating=rating, subject=subject, comment=comment)
            review_count = product.reviews.filter(status='active').count()
            review_html = render_to_string('store/components/review_item.html', {'review': review, 'user': user}, request=request)

            return JsonResponse({'status':'success','message':'Review submitted successfully','review_count': review_count,'review_html': review_html})

        except Exception as e:
            logger.error(f"ProductReviewView error: {e}", exc_info=True)
            return JsonResponse({'status':'error','message':'Unable to submit review'})


# =========================================================
# SHOP VIEW WITH PAGINATION & SORT
# =========================================================
@method_decorator(never_cache, name='dispatch')
class ShopView(generic.View):
    def get(self, request):
        try:
            per_page_options = [3,6,12]
            sort_options = ['latest','new','upcoming']

            products = Product.objects.filter(status='active').annotate(
                total_variant_stock=Sum('variants__available_stock', filter=Q(variants__status='active')),
                avg_rate=Avg('reviews__rating', filter=Q(reviews__status='active'))
            ).filter(Q(available_stock__gt=0) | Q(total_variant_stock__gt=0)) \
             .select_related('category','brand').prefetch_related('variants')

            banners = Slider.objects.filter(slider_type='add', status='active')[:1]

            try:
                per_page = int(request.GET.get('per_page') or 3)
                page_number = int(request.GET.get('page') or 1)
            except ValueError:
                per_page = 3
                page_number = 1

            sort_by = request.GET.get('sort','latest')
            if sort_by == 'upcoming':
                products = products.filter(deadline__gt=timezone.now()).order_by('deadline')
            else:
                sort_map = {'latest':'-created_at', 'new':'created_at'}
                products = products.order_by(sort_map.get(sort_by,'-created_at'))

            paginator = Paginator(products, per_page)
            page_obj = paginator.get_page(page_number)

            context = {
                'products': page_obj, 'banners': banners, 'page_obj': page_obj,
                'per_page_options': per_page_options, 'sort_options': sort_options,
                'selected_per_page': per_page, 'selected_sort': sort_by
            }

            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'html': render_to_string('store/components/grid.html', context, request=request),
                    'pagination_html': render_to_string('store/components/pagination.html', context, request=request)
                })

            return render(request, 'store/shop.html', context)

        except Exception as e:
            logger.error(f"ShopView error: {e}", exc_info=True)
            return render(request, 'store/shop.html', {'products': [], 'banners': [], 'page_obj': None})


# =========================================================
# CATEGORY PRODUCTS VIEW
# =========================================================
@method_decorator(never_cache, name='dispatch')
class CategoryProductView(generic.View):
    def get(self, request, slug, id):
        category = get_object_or_404(Category, slug=slug, id=id)

        products = Product.objects.filter(category=category, status='active').annotate(
            total_variant_stock=Sum('variants__available_stock', filter=Q(variants__status='active')),
            avg_rate=Avg('reviews__rating', filter=Q(reviews__status='active'))
        ).filter(Q(available_stock__gt=0) | Q(total_variant_stock__gt=0)) \
         .select_related('brand','category').prefetch_related('variants')

        sort_options = ['latest','new','upcoming']
        sort_by = request.GET.get('sort','latest')
        if sort_by == 'upcoming': products = products.filter(deadline__gt=timezone.now()).order_by('deadline')
        elif sort_by == 'new': products = products.order_by('created_at')
        else: products = products.order_by('-created_at')

        per_page_options = [3,6,12,24]
        try: per_page = int(request.GET.get('per_page'))
        except: per_page = 3
        if per_page not in per_page_options: per_page = 3

        paginator = Paginator(products, per_page)
        page_obj = paginator.get_page(request.GET.get('page'))
        banners = Slider.objects.filter(slider_type='add', status='active')[:1]

        context = {
            'category': category, 'products': page_obj, 'page_obj': page_obj,
            'banners': banners, 'per_page_options': per_page_options, 'sort_options': sort_options,
            'selected_per_page': per_page, 'selected_sort': sort_by
        }

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'html': render_to_string('store/components/grid.html', context, request=request),
                'pagination_html': render_to_string('store/components/pagination.html', context, request=request)
            })

        return render(request, 'store/category-product.html', context)


# =========================================================
# SEARCH VIEWS
# =========================================================
@method_decorator(never_cache, name='dispatch')
class SearchingView(generic.View):
    def post(self, request):
        query = request.POST.get('q','').strip()
        category_id = request.POST.get('category')

        products = Product.objects.filter(status='active').annotate(
            total_variant_stock=Sum('variants__available_stock', filter=Q(variants__status='active')),
            avg_rate=Avg('reviews__rating', filter=Q(reviews__status='active'))
        ).filter(Q(available_stock__gt=0) | Q(total_variant_stock__gt=0)) \
         .select_related('category','brand').prefetch_related('variants')

        if not query and not category_id: products = Product.objects.none()
        if query: products = products.filter(Q(title__icontains=query) | Q(keyword__icontains=query))
        if category_id: products = products.filter(category_id=category_id)

        return render(request, 'store/searching.html', {'products': products, 'query': query, 'selected_category': category_id})


@method_decorator(never_cache, name='dispatch')
class AutoSearchComplete(generic.View):
    def get(self, request):
        term = request.GET.get('term','').strip()
        results = []

        if term:
            products = Product.objects.filter(status='active', available_stock__gt=0, title__icontains=term)[:5]
            product_ids = [p.id for p in products]
            images_map = {img.product_id: img.image.url for img in ImageGallery.objects.filter(product_id__in=product_ids, status='active').order_by('id')}
            for p in products:
                results.append({
                    'title': p.title,
                    'price': f"{p.sale_price:.2f}",
                    'image': images_map.get(p.id,''),
                    'url': f"/product/{p.slug}/{p.id}/"
                })

        return JsonResponse(results, safe=False)
