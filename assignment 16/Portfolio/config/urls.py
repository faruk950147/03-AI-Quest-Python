from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    # Website URLs
    path('', include('home.urls')),
    path('about/', include('about.urls')),
    path("resume/", include("resume.urls")),
    path("service/", include("service.urls")),
    path("portfolio/", include("portfolio.urls")),
    path("contact/", include("contact.urls")),
    path('account/', include('account.urls')),
    
    # API endpoints    
    path("api/home/", include("home.api_urls")),
    path("api/about/", include("about.api_urls")),
    path("api/resume/", include("resume.api_urls")),
    path("api/service/", include("service.api_urls")),
    path("api/portfolio/", include("portfolio.api_urls")),
    path("api/contact/", include("contact.api_urls")),
    path('api/account/', include('account.api_urls')),

    # JWT Auth
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    # Admin site
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)