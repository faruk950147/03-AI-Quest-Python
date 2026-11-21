
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from . import views


urlpatterns = [
    path("", views.home, name="home"),

    path(
        "login/",
        LoginView.as_view(template_name="login.html"),
        name="login"
    ),

    path(
        "logout/",
        LogoutView.as_view(),
        name="logout"
    ),

    path(
        "register/",
        views.register,
        name="register"
    ),

    path(
        "stock-data/",
        views.fetch_stock_data,
        name="fetch_stock_data"
    ),

    path(
        "api/stock-data/",
        views.stock_data_api,
        name="stock_data_api"
    ),

    path(
        "delete-stock/",
        views.delete_stock,
        name="delete_stock"
    ),

    path(
        "refresh-stock-prices/",
        views.refresh_stock_prices,
        name="refresh_stock_prices"
    ),
]
