from django.urls import path
from store.views import (
    HomeView, SingleProductView, CategoryProductView, BrandProductView
)
urlpatterns = [
    # Define your URL patterns here
    path('', HomeView.as_view(), name='home'),
    path('single-product/<str:slug>/<int:id>/', SingleProductView.as_view(), name='single-product'),
    path('category-product/<str:slug>/<int:id>/', CategoryProductView.as_view(), name='category-product'),
    path('category-product/<str:slug>/<int:id>/<str:data>/', CategoryProductView.as_view(), name='category-filter'),
    path('brand-product/<str:slug>/<int:id>/', BrandProductView.as_view(), name='brand-product'),
]




    
