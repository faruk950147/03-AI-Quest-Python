from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.template.loader import render_to_string
from django.http import JsonResponse
from store.models import Category, Brand, Product, Slider


# Create your views here.
@method_decorator(never_cache, name='dispatch')
class HomeView(generic.View):
    """
    # 1. Case-insensitive substring search 
    # Example: "Pant", "pant", "PANT" — all will match
    products = Product.objects.filter(category__title__icontains='pant')

    # 2. Case-sensitive substring search
    # Example: only "pant" will match; "PANT" or "Pant" will not
    products = Product.objects.filter(category__title__contains='pant')

    # 3. Case-insensitive exact match 
    # Example: "pant", "PANT", "Pant" — all will match, 
    # but "pants" or "pant123" will not
    products = Product.objects.filter(category__title__iexact='pant')

    # 4. Multiple match using 'in' lookup
    # This returns all products whose category title is either 
    # 'pant', 'shirt', or 'howdy'
    products = Product.objects.filter(category__title__in=['pant', 'shirt', 'howdy'])        
    shirts = Product.objects.filter(category__title__in="SHIRT", status='ACTIVE').select_related('category')
    """
    def get(self, request):
        sliders = Slider.objects.filter(status='ACTIVE')
        gents_pants = Product.objects.filter(category__title__contains='GENT PANTS', status='ACTIVE')
        borkhas = Product.objects.filter(category__title__contains='BORKHA', status='ACTIVE')
        baby_fashions = Product.objects.filter(category__title__contains='BABY FASHION', status='ACTIVE')

        context = {
            'sliders': sliders, 
            'gents_pants': gents_pants, 
            'borkhas': borkhas, 
            'baby_fashions': baby_fashions,
        }
        return render(request, "store/home.html", context)

@method_decorator(never_cache, name='dispatch')
class SingleProductView(generic.View):
    def get(self, request, slug, id):
        product = get_object_or_404(Product, slug=slug, id=id)
        context = {
            'product': product,
        }
        return render(request, "store/single-product.html", context)

@method_decorator(never_cache, name='dispatch')
class CategoryProductView(generic.View):
    def get(self, request, slug, id):
        # Category fetch
        category = get_object_or_404(Category, slug=slug, id=id)

        # Products fetch
        products = Product.objects.filter(category=category, status='ACTIVE')

        # Brands fetch (distinct)
        brands = Brand.objects.filter(product__category=category).distinct()

        # Brand filter
        selected_brand = request.GET.get('brand')
        if selected_brand:
            products = products.filter(brand__id=selected_brand)

        # Price filter
        price_filter = request.GET.get('price')
        if price_filter == 'below_20k':
            products = products.filter(sale_price__lt=20000)
        elif price_filter == 'above_20k':
            products = products.filter(sale_price__gte=20000)

        context = {
            'category': category,
            'products': products,
            'brands': brands,
            'selected_brand': int(selected_brand) if selected_brand else None,
            'price_filter': price_filter,
        }

        # Normal render without AJAX
        return render(request, "store/category-product.html", context)

@method_decorator(never_cache, name='dispatch')
class ProductsListView(generic.View):
    def get(self, request):
        products = Product.objects.filter(status='ACTIVE')
        context = {
            'products': products,
        }
        return render(request, "store/products-list.html", context)