from django.urls import path
from store.views import (
    HomeView, SingleProductView, CategoryProductView, ProductsListView
)
urlpatterns = [
    # Define your URL patterns here
    path('', HomeView.as_view(), name='home'),
    path('single-product/<str:slug>/<int:id>/', SingleProductView.as_view(), name='single-product'),
    path('category-product/<str:slug>/<int:id>/', CategoryProductView.as_view(), name='category-product'),
    path('products-lists>/', ProductsListView.as_view(), name='products-lists'),

]




    
