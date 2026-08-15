from django.urls import path
from collage.views import CollageView

urlpatterns = [
    path('', CollageView.as_view(), name='collage'),
]
