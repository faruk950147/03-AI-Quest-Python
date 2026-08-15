from django.urls import path
from map.views import MapView

urlpatterns = [
    path('', MapView.as_view(), name='map'),
]
