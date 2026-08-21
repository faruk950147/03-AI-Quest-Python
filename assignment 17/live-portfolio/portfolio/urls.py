from django.urls import path

from portfolio.views import (
    PortfolioView,
)

urlpatterns = [
    path('portfolio/', PortfolioView.as_view(), name='portfolio'),
]
