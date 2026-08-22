from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('store.urls')),
    path('cart/', include('cart.urls')),
    path('checkout/', include('checkout.urls')),
    path('accounts/', include('accounts.urls')),
    path('admin/', admin.site.urls),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)