from django.urls import path
from store.api_views import *

urlpatterns = [
    path('', APIRoot.as_view()),
    path('home/', HomeViewAPI.as_view()),
    path('product/detail/<str:slug>/<int:id>/', ProductDetailViewAPI.as_view()),
    path('get/variant/by/size/', GetVariantBySizeViewAPI.as_view()),
    path('get/variant/by/color/', GetVariantByColorViewAPI.as_view()),
    path('get/filter/products/', GetFilterProductsViewAPI.as_view()),
    path('shopping/', ShopViewAPI.as_view()),
    path('category/products/', CategoryProductViewAPI.as_view()),
    path('product/reviews/', ProductReviewViewAPI.as_view()),
    path('searching/products/', SearchingViewAPI.as_view()),
    path('auto/search/complete/', AutoSearchCompleteAPI.as_view())
]