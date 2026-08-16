from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from store.views import HomeView, SingleProductView, CategoryProductView, SearchProductView, GetFilterProductsView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('single-product/<str:slug>/<int:id>/', SingleProductView.as_view(), name='single-product'),
    path('category-product/<str:slug>/<int:id>/', CategoryProductView.as_view(), name='category-product'),
    path('get-filter-products/', csrf_exempt(GetFilterProductsView.as_view()), name='get-filter-products'),
    path('search-product/', SearchProductView.as_view(), name='search-product'),
]
