from django.contrib import admin
from cart.models import Cart, Wishlist

# =========================================================
# CART ADMIN
# =========================================================
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user', 'product', 'variant', 'quantity', 'paid', 'stored_unit_price',
        'unit_price', 'subtotal',
        'created_at', 'updated_at'
    )
    search_fields = ('user__username', 'product__title', 'variant__id')
    readonly_fields = ('unit_price', 'subtotal', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')


# =========================================================
# WISHLIST ADMIN
# =========================================================
@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'variant', 'created_at', 'updated_at')
    search_fields = ('user__username', 'product__title', 'variant__id')
    readonly_fields = ('created_at', 'updated_at')
