from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.db.models import Q
from store.models import Category, Brand, Product, Slider, LiveSales
from cart.models import Cart
import logging

logger = logging.getLogger('project')


@method_decorator(never_cache, name='dispatch')
class HomeView(generic.View):
    def get(self, request):
        sliders = Slider.objects.filter(status='ACTIVE')
        live_sales = LiveSales.objects.filter(status='ACTIVE')
        gents_pants = Product.objects.filter(category__title__contains='GENT PANTS', status='ACTIVE')
        borkhas = Product.objects.filter(category__title__contains='BORKHA', status='ACTIVE')
        baby_fashions = Product.objects.filter(category__title__contains='BABY FASHION', status='ACTIVE')

        logger.info(f"User {request.user if request.user.is_authenticated else 'Anonymous'} visited Home page")

        context = {
            'sliders': sliders, 
            'live_sales': live_sales,
            'gents_pants': gents_pants, 
            'borkhas': borkhas, 
            'baby_fashions': baby_fashions,
        }
        return render(request, "store/home.html", context)

@method_decorator(never_cache, name='dispatch')
class SingleProductView(generic.View):
    def get(self, request, slug, id):
        product = get_object_or_404(Product, slug=slug, id=id)
  
        logger.info(f"viewed product {product.id} - {product.title}")

        context = {
            'product': product,
        }
        return render(request, "store/single-product.html", context)

@method_decorator(never_cache, name='dispatch')
class CategoryProductView(generic.View):
    def get(self, request, slug, id):
        category = get_object_or_404(Category, slug=slug, id=id)
        products = Product.objects.filter(category=category, status='ACTIVE')
        brands = Brand.objects.filter(product__category=category).distinct()
        
        selected_brand = request.GET.get('brand')
        price_filter = request.GET.get('price')

        if selected_brand:
            products = products.filter(brand__id=selected_brand)
        if price_filter == 'below_20k':
            products = products.filter(sale_price__lt=20000)
        elif price_filter == 'above_20k':
            products = products.filter(sale_price__gte=20000)

        logger.info(
            f"User {request.user if request.user.is_authenticated else 'Anonymous'} viewed category {category.id} with brand={selected_brand} and price_filter={price_filter}"
        )

        context = {
            'products': products,
            'category': category,
            'brands': brands,
            'selected_brand': int(selected_brand) if selected_brand else None,
            'price_filter': price_filter,
        }

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            html = render_to_string('store/product_grid.html', context)
            return JsonResponse({'html': html})

        return render(request, 'store/category-product.html', context)
    
@method_decorator(never_cache, name='dispatch')
class SearchProductView(generic.View):
    def post(self, request):
        q = request.POST.get('q', '').strip()

        if q:
            products = Product.objects.filter(title__icontains=q)
        else:
            products = Product.objects.none()

        logger.info(
            f"User {request.user if request.user.is_authenticated else 'Anonymous'} searched for '{q}' and found {products.count()} products"
        )

        return render(request, 'store/search-results.html', {
            'products': products,
            'count_products': products.count(),
        })
