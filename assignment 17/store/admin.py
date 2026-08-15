from django.contrib import admin
from store.models import (
    Category, Brand, Color, Size, Product, ProductVariant,
    ImageGallery, Slider, Review, AcceptancePayment
)

# =========================================================
# IMAGE TAG DISPLAY MIXIN
# =========================================================
class ImageTagAdminMixin:
    readonly_fields = ('image_tag',)
    def image_tag(self, obj):
        return obj.image_tag() if hasattr(obj, 'image_tag') else None
    image_tag.short_description = 'Image'

# =========================================================
# 01. CATEGORY ADMIN
# =========================================================
@admin.register(Category)
class CategoryAdmin(ImageTagAdminMixin, admin.ModelAdmin):
    list_display = ('id', 'parent', 'title', 'slug', 'status', 'is_featured', 'image_tag', 'created_at', 'updated_at')
    search_fields = ('title', 'keyword', 'description')
    list_filter = ('status', 'is_featured')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_at', 'updated_at', 'image_tag')
    fields = ('parent', 'title', 'slug', 'keyword', 'description', 'image', 'status', 'is_featured', 'image_tag')

# =========================================================
# 02. BRAND ADMIN
# =========================================================
@admin.register(Brand)
class BrandAdmin(ImageTagAdminMixin, admin.ModelAdmin):
    list_display = ('id', 'title', 'slug', 'status', 'is_featured', 'image_tag', 'created_at', 'updated_at')
    search_fields = ('title', 'keyword', 'description')
    list_filter = ('status', 'is_featured')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_at', 'updated_at', 'image_tag')
    fields = ('title', 'slug', 'keyword', 'description', 'image', 'status', 'is_featured', 'image_tag')

# =========================================================
# 03. COLOR ADMIN
# =========================================================
@admin.register(Color)
class ColorAdmin(ImageTagAdminMixin, admin.ModelAdmin):
    list_display = ('id', 'title', 'code', 'color_tag', 'status', 'created_at', 'updated_at')
    search_fields = ('title', 'code')
    list_filter = ('status',)
    readonly_fields = ('created_at', 'updated_at', 'color_tag')
    fields = ('title', 'code', 'status', 'color_tag')

# =========================================================
# 04. SIZE ADMIN
# =========================================================
@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'code', 'status', 'created_at', 'updated_at')
    search_fields = ('title', 'code')
    list_filter = ('status',)
    readonly_fields = ('created_at', 'updated_at')
    fields = ('title', 'code', 'status')

# =========================================================
# INLINE FOR PRODUCT VARIANTS AND IMAGE GALLERY
# =========================================================
class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1
    readonly_fields = ('image_tag', 'created_at', 'updated_at')
    fields = ('color', 'size', 'sku', 'variant_price', 'available_stock', 'status', 'image_id', 'image_tag')

class ImageGalleryInline(admin.TabularInline):
    model = ImageGallery
    extra = 1
    readonly_fields = ('image_tag', 'created_at', 'updated_at')
    fields = ('image', 'status', 'image_tag')

# =========================================================
# 05. PRODUCT ADMIN
# =========================================================
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'slug', 'category', 'brand', 'variant', 'old_price', 'sale_price', 'discount_percent', 'available_stock', 'sold', 'visited', 'status', 'is_featured', 'created_at', 'updated_at')
    search_fields = ('title', 'slug', 'keyword', 'description', 'tag', 'prev_des', 'add_des', 'short_des', 'long_des')
    list_filter = ('status', 'is_featured', 'category', 'brand', 'variant')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ProductVariantInline, ImageGalleryInline]
    list_editable = ('available_stock',)
    readonly_fields = ('created_at', 'updated_at')
    fields = (
        'category', 'brand', 'variant', 'title', 'slug',
        'old_price', 'sale_price', 'discount_percent', 'sold', 'visited',
        'prev_des', 'add_des', 'short_des', 'long_des', 'keyword', 'description', 'tag',
        'deadline', 'is_deadline', 'is_featured', 'status'
    )

# =========================================================
# 06. PRODUCT VARIANT ADMIN
# =========================================================
@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'product', 'color', 'size', 'sku', 'variant_price',
        'available_stock', 'status', 'image_id', 'image_tag', 'created_at', 'updated_at'
    )
    search_fields = ('sku', 'product__title')
    list_filter = ('status', 'color', 'size')
    readonly_fields = ('image_tag', 'created_at', 'updated_at')
    fields = (
        'product', 'color', 'size', 'sku', 'variant_price', 
        'available_stock', 'status', 'image_id', 'image_tag'
    )

# =========================================================
# 07. IMAGE GALLERY ADMIN
# =========================================================
@admin.register(ImageGallery)
class ImageGalleryAdmin(ImageTagAdminMixin, admin.ModelAdmin):
    list_display = ('id', 'product', 'image_tag', 'status', 'created_at', 'updated_at')
    list_filter = ('status', 'product')
    readonly_fields = ('created_at', 'updated_at', 'image_tag')
    fields = ('product', 'image', 'status', 'image_tag')

# =========================================================
# 08. SLIDER ADMIN
# =========================================================
@admin.register(Slider)
class SliderAdmin(ImageTagAdminMixin, admin.ModelAdmin):
    list_display = ('id', 'title', 'slider_type', 'product', 'sub_title', 'paragraph', 'status', 'image_tag', 'created_at', 'updated_at')
    search_fields = ('title', 'sub_title', 'paragraph')
    list_filter = ('status', 'slider_type')
    readonly_fields = ('created_at', 'updated_at', 'image_tag')
    fields = ('product', 'slider_type', 'title', 'sub_title', 'paragraph', 'image', 'status', 'image_tag')

# =========================================================
# 09. REVIEW ADMIN
# =========================================================
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'user', 'subject', 'comment', 'rating', 'status', 'created_at', 'updated_at')
    search_fields = ('subject', 'comment', 'user__username', 'product__title')
    list_filter = ('status', 'rating')
    readonly_fields = ('created_at', 'updated_at')
    fields = ('product', 'user', 'subject', 'comment', 'rating', 'status')

# =========================================================
# 10. ACCEPTANCE PAYMENT ADMIN
# =========================================================
@admin.register(AcceptancePayment)
class AcceptancePaymentAdmin(ImageTagAdminMixin, admin.ModelAdmin):
    list_display = ('id', 'title', 'status', 'is_featured', 'image_tag', 'help_time', 'created_at', 'updated_at')
    search_fields = ('title',)
    list_filter = ('status', 'is_featured')
    readonly_fields = ('created_at', 'updated_at', 'image_tag')
    fields = ('title', 'image', 'help_time', 'status', 'is_featured', 'image_tag')
