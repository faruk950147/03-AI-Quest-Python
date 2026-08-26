from django.urls import path
from store.views import (
    HomeView, ProductView, GetVariantBySizeView, GetVariantByColorView,
    GetFilterProductsView, ShopView, CategoryProductView,
    ProductReviewView, SearchingView, AutoSearchComplete
)
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('product/detail/<str:slug>/<int:id>/', ProductView.as_view(), name='product-detail'),
    path('get/variant/by/size/', GetVariantBySizeView.as_view(), name='get-variant-by-size'),
    path('get/variant/by/color/', GetVariantByColorView.as_view(), name='get-variant-by-color'),
    path('get/filter/products/', GetFilterProductsView.as_view(), name='get-filter-products'),
    path('shopping/', ShopView.as_view(), name="shopping"),
    path('category/products/<str:slug>/<int:id>/', CategoryProductView.as_view(), name='category-products'),
    path('product/review/', ProductReviewView.as_view(), name='product-review'),
    path('auto/searching/product/', AutoSearchComplete.as_view(), name='auto-searching-product'),
    path('searching/product/', SearchingView.as_view(), name='searching-product'),
]