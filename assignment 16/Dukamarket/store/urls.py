from django.urls import path
from store.views import(
    HomeView,
    ProductDetailView,
    ProductReviewView,
    ShopView,
    GetFilterProductsView,
    GetVariantBySizeView,
    GetVariantByColorView,
    SearchingView,
    AutoSearchComplete,
    CategoryProductView
)
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('product/<slug:slug>/<int:id>/', ProductDetailView.as_view(), name='product-detail'),
    path('get-variant-by-size/', GetVariantBySizeView.as_view(), name='get-variant-by-size'),
    path('get-variant-by-color/', GetVariantByColorView.as_view(), name='get-variant-by-color'),
    path('get-filter-products/', GetFilterProductsView.as_view(), name='get-filter-products'),
    path('product-review/', ProductReviewView.as_view(), name='product-review'),
    path('shop/', ShopView.as_view(), name='shop'),
    path('searching-product/', SearchingView.as_view(), name='searching-product'),
    path('auto-searching-product/', AutoSearchComplete.as_view(), name='auto-searching-product'),
    path('category-product/<slug:slug>/<int:id>/', CategoryProductView.as_view(), name='category-product'),
]
