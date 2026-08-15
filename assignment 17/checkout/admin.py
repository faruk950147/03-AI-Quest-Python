from django.contrib import admin
from .models import Coupon, Checkout, CheckoutItem


# =============================
# Coupon Admin
# =============================
@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'code', 'discount_percent', 'max_discount_amount',
        'used_count', 'max_usage', 'active',
        'start_date', 'end_date', 'created_at', 'updated_at'
    )
    list_filter = ('active', 'start_date', 'end_date')
    search_fields = ('code',)
    readonly_fields = ('created_at', 'updated_at')


# =============================
# Checkout Item Inline
# =============================
class CheckoutItemInline(admin.TabularInline):
    model = CheckoutItem
    extra = 0
    readonly_fields = ('product', 'variant', 'quantity', 'unit_price', 'subtotal', 'created_at', 'updated_at')
    can_delete = False


# =============================
# Checkout Admin
# =============================
@admin.register(Checkout)
class CheckoutAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user', 'shipping', 'coupon', 'payment_method', 'status', 'is_finalized', 'paid_at', 
        'total_amount', 'discount_amount', 'final_amount','created_at', 'updated_at'
    )
    list_filter = ('status', 'shipping', 'coupon', 'is_finalized', 'created_at', 'updated_at')
    search_fields = ('user__username',)
    readonly_fields = (
        'user', 'shipping', 'coupon', 'payment_method', 'is_finalized', 'paid_at', 
        'total_amount', 'discount_amount', 'final_amount','created_at', 'updated_at'
    )
    inlines = [CheckoutItemInline]


# =============================
# Checkout Item Admin (separate view)
# =============================
@admin.register(CheckoutItem)
class CheckoutItemAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'checkout', 'product', 'variant',
        'quantity', 'unit_price', 'subtotal', 'created_at', 'updated_at'
    )
    list_filter = ('created_at',)
    search_fields = ('product__title',)
    readonly_fields = ('checkout', 'product', 'variant', 'quantity', 'unit_price', 'subtotal', 'created_at', 'updated_at')

