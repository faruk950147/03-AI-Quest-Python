from django.shortcuts import render, get_object_or_404
from django.views import generic
from store.models import Category, Brand, Product, Slider


# Create your views here.
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

class SingleProductView(generic.View):
    def get(self, request, slug, id):
        product = get_object_or_404(Product, slug=slug, id=id)
        context = {
            'product': product,
        }
        return render(request, "store/single-product.html", context)
    
class CategoryProductView(generic.View):
    def get(self, request, slug, id, data=None):
        category = get_object_or_404(Category, slug=slug, id=id)
        products = Product.objects.filter(category=category, status='ACTIVE')
        brands = Brand.objects.filter(product__category=category, product__status='ACTIVE').distinct().order_by('title')

        if data:
            brand_slugs = list(brands.values_list('slug', flat=True))
            
            if data in brand_slugs:
                products = products.filter(brand__slug=data)
            elif data == 'above':
                products = products.filter(sale_price__gte=20000)
            elif data == 'below':
                products = products.filter(sale_price__lt=20000)
            else:
                products = Product.objects.none()

        context = {
            'products': products,
            'category': category,
            'brands': brands,
            'current_data': data,
        }
        return render(request, "store/category-product.html", context)
    
class BrandProductView(generic.View):
    def get(self, request, slug, id):
        brand = get_object_or_404(Brand, slug=slug, id=id)
        brand_products = Product.objects.filter(brand=brand, status='ACTIVE')
        context = {
            'brand_products': brand_products,
        }
        return render(request, "store/brand-product.html", context)
    
    