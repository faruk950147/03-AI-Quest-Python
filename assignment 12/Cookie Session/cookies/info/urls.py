from django.urls import path
from info.views import SetCookie, InfoDetailView

urlpatterns = [
    path('set-cookie/', SetCookie.as_view(), name='set-cookie'),
    path('detail/<int:id>/', InfoDetailView.as_view(), name='info-detail'),
]
