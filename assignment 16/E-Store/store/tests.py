from django.conf import settings
from django.test import RequestFactory, SimpleTestCase, override_settings

from cart.api_views import APIRoot as CartAPIRoot
from store.api_views import APIRoot as StoreAPIRoot
from store.views import RootView


@override_settings(BASE_URL="https://shop.example.test")
class BaseUrlSyncTests(SimpleTestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_store_root_view_uses_configured_base_url(self):
        response = RootView.as_view()(self.factory.get("/"), None)
        self.assertContains(response, "https://shop.example.test")

    def test_store_root_api_uses_configured_base_url(self):
        response = StoreAPIRoot.as_view()(self.factory.get("/api/store/"), None)
        self.assertIn("https://shop.example.test", response.data["home"])

    def test_cart_root_api_uses_configured_base_url(self):
        response = CartAPIRoot.as_view()(self.factory.get("/api/cart/"), None)
        self.assertIn("https://shop.example.test", response.data["cart_detail"])

    def test_settings_are_localhost_safe_when_debug_is_on(self):
        self.assertFalse(settings.SESSION_COOKIE_SECURE)
        self.assertFalse(settings.CSRF_COOKIE_SECURE)
