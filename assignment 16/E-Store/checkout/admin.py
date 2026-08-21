from django.contrib import admin
from unfold.admin import ModelAdmin

from checkout.models import Shipping, Coupon, Checkout, CheckoutItem


@admin.register(Shipping)
class ShippingAdmin(ModelAdmin):
    list_display = (
        'id',
        'user',
        'shipping_choice',
        'name',
        'country',
        'city',
        'home_city',
        'zip_code',
        'phone',
        'created_at',
        'updated_at',
    )

    list_filter = (
        'shipping_choice',
        'country',
        'city',
        'created_at',
    )

    search_fields = (
        'user__username',
        'user__email',
        'name',
        'phone',
        'address',
        'city',
        'country',
        'zip_code',
    )

    readonly_fields = (
        'created_at',
        'updated_at',
    )

    ordering = ('-id',)


# =============================
# Coupon Admin
# =============================
@admin.register(Coupon)
class CouponAdmin(ModelAdmin):
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
class CheckoutAdmin(ModelAdmin):
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
class CheckoutItemAdmin(ModelAdmin):
    list_display = (
        'id', 'checkout', 'product', 'variant',
        'quantity', 'unit_price', 'subtotal', 'created_at', 'updated_at'
    )
    list_filter = ('created_at',)
    search_fields = ('product__title',)
    readonly_fields = ('checkout', 'product', 'variant', 'quantity', 'unit_price', 'subtotal', 'created_at', 'updated_at')

