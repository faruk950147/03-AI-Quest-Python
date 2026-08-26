from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    # Website URLs
    path('', include('home.urls')),
    path('about/', include('about.urls')),
    path("resume/", include("resume.urls")),
    path("service/", include("service.urls")),
    path("portfolio/", include("portfolio.urls")),
    path("contact/", include("contact.urls")),
    
    # API endpoints    
    path("api/home/", include("home.api_urls")),
    path("api/about/", include("about.api_urls")),
    path("api/resume/", include("resume.api_urls")),
    path("api/service/", include("service.api_urls")),
    path("api/portfolio/", include("portfolio.api_urls")),
    path("api/contact/", include("contact.api_urls")),

    # Admin site
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)