from django.contrib import admin
from unfold.admin import ModelAdmin

from store.models import (
    Category,
    Brand,
    Color,
    Size,
    Product,
    Gallery,
    VariantOption,
    Slider,
    Review,
    AllowPayment,
)


# ======================== CATEGORY ========================
@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = (
        'id', 'parent', 'title', 'slug', 'keyword',
        'description', 'icon', 'image_tag', 'is_featured',
        'status', 'created_at', 'updated_at'
    )
    
    list_editable = (
        'is_featured',
        'status',
    )

    search_fields = (
        'title', 'keyword', 'description'
    )

    list_filter = (
        'status', 'is_featured'
    )

    readonly_fields = (
        'created_at',
        'updated_at',
        'image_tag',
    )

    fieldsets = (
        (None, {
            "fields": (
                'parent', 'title', 'slug',
                'keyword', 'description', 'icon',
                'image', 'is_featured',
                'status',
            ),
        }),
    )

# ======================= BRAND ========================
@admin.register(Brand)
class BrandAdmin(ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = (
        'id', 'title', 'slug', 'keyword',
        'description', 'image_tag',
        'is_featured', 'status',
        'created_at', 'updated_at'
    )
    
    list_editable = (
        'is_featured',
        'status',
    )

    search_fields = (
        'title', 'keyword', 'description'
    )

    list_filter = (
        'is_featured', 'status',
    )

    prepopulated_fields = {
        'slug': ('title',)
    }

    readonly_fields = (
        'created_at',
        'updated_at',
        'image_tag',
    )

    fieldsets = (
        (None, {
            "fields": (
                'title', 'slug', 'keyword',
                'description', 'image',
                'is_featured', 'status',
            ),
        }),
    )

# ======================= COLOR ========================
@admin.register(Color)
class ColorAdmin(ModelAdmin):
    list_display = (
        'id', 'title', 'code',
        'color_tag', 'status',
        'created_at', 'updated_at'
    )
    
    list_editable = (
        'status',
    )

    search_fields = (
        'title', 'code'
    )

    list_filter = (
        'status',
    )

    readonly_fields = (
        'created_at',
        'updated_at',
    )

    fieldsets = (
        (None, {
            "fields": (
                'title', 'code',
                'status',
            ),
        }),
    )

# ======================= SIZE ========================
@admin.register(Size)
class SizeAdmin(ModelAdmin):
    list_display = (
        'id', 'title', 'code',
        'status', 'created_at',
        'updated_at'
    )
    
    list_editable = (
        'status',
    )

    search_fields = (
        'title', 'code'
    )

    list_filter = (
        'status',
    )

    readonly_fields = (
        'created_at',
        'updated_at',
    )

    fieldsets = (
        (None, {
            "fields": (
                'title', 'code',
                'status',
            ),
        }),
    )

# ======================= VARIANT OPTIONS INLINE ========================
class VariantOptionInline(admin.TabularInline):
    model = VariantOption
    extra = 1

    readonly_fields = (
        'created_at',
        'updated_at',
    )

    fields = (
        'color', 'size', 'image_id', 'sku',
        'variant_price', 'stock', 'status',
    )

# ====================== IMAGE GALLERY INLINE ========================
class GalleryInline(admin.TabularInline):
    model = Gallery
    extra = 1

    readonly_fields = (
        'created_at',
        'updated_at',
    )

    fields = (
        'image',
        'status',
    )

# ======================= PRODUCT ========================
@admin.register(Product)
class ProductAdmin(ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = (
        'id', 'category', 'brand',
        'variants_type', 'title',
        'slug', 'tag', 'old_price',
        'sale_price', 'discount',
        'stock', 'sold', 'visited',
        'prev_des', 'add_des',
        'short_des', 'long_des',
        'keyword', 'description',
        'deadline', 'is_deadline',
        'is_featured', 'status',
        'created_at', 'updated_at'
    )
    
    list_editable = (
        'category', 'brand',
        'variants_type', 'old_price',
        'sale_price', 'discount',
        'stock', 'sold', 'visited',
        'is_deadline', 'is_featured',
        'status',
    )

    search_fields = (
        'title', 'slug', 'keyword',
        'description', 'tag',
        'prev_des', 'add_des',
        'short_des', 'long_des',
    )

    list_filter = (
        'category', 'brand',
        'variants_type', 'deadline',
        'is_deadline', 'is_featured',
        'status',
    )

    list_select_related = (
        'category',
        'brand',
    )

    inlines = [
        VariantOptionInline,
        GalleryInline,
    ]

    readonly_fields = (
        'created_at',
        'updated_at',
    )

    fieldsets = (
        (None, {
            "fields": (
                'category', 'brand',
                'variants_type', 'title',
                'slug', 'tag',
                'old_price', 'sale_price',
                'discount', 'stock',
                'sold', 'visited',
                'prev_des', 'add_des',
                'short_des', 'long_des',
                'keyword', 'description',
                'deadline', 'is_deadline',
                'is_featured', 'status'
            ),
        }),
    )

# ======================= GALLERY ========================
@admin.register(Gallery)
class GalleryAdmin(ModelAdmin):

    list_display = (
        'id', 'product', 'image_tag',
        'status', 'created_at',
        'updated_at'
    )
    
    list_editable = (
        'status',
    )

    search_fields = (
        'product__title',
    )

    list_filter = (
        'status',
    )

    readonly_fields = (
        'created_at',
        'updated_at',
        'image_tag',
    )

    fieldsets = (
        (None, {
            "fields": (
                'product', 'image',
                'status',
            ),
        }),
    )

# ======================= VARIANT OPTIONS ========================
@admin.register(VariantOption)
class VariantOptionsAdmin(ModelAdmin):
    list_display = (
        'id', 'product', 'color',
        'size', 'image_id', 'sku', 'variant_price',
        'stock', 'status',
        'created_at', 'updated_at'
    )
    
    list_editable = (
        'image_id',
        'stock',
        'status',
    )

    search_fields = (
        'product__title',
        'color__title',
        'size__title',
        'sku'
    )

    list_filter = (
        'status',
    )

    list_select_related = (
        'product',
        'color',
        'size',
    )

    readonly_fields = (
        'created_at',
        'updated_at',
    )

    fieldsets = (
        (None, {
            "fields": (
                'product', 'color',
                'size', 'image_id', 'sku',
                'variant_price', 'stock',
                'status'
            ),
        }),
    )

# ====================== SLIDER ========================
@admin.register(Slider)
class SliderAdmin(ModelAdmin):
    list_display = (
        'id', 'product',
        'slider_type', 'headline',
        'button', 'image_tag',
        'status', 'created_at',
        'updated_at'
    )
    
    list_editable = (
        'status',
    )

    search_fields = (
        'product__title',
        'slider_type',
        'headline',
        'button'
    )

    list_filter = (
        'status',
        'slider_type'
    )

    readonly_fields = (
        'created_at',
        'updated_at',
        'image_tag',
    )

    fieldsets = (
        (None, {
            "fields": (
                'product', 'slider_type',
                'headline', 'button',
                'image', 'status',
            ),
        }),
    )

# ======================= REVIEW ========================
@admin.register(Review)
class ReviewAdmin(ModelAdmin):
    list_display = (
        'id', 'product', 'user',
        'subject', 'comment',
        'rating', 'status',
        'created_at', 'updated_at'
    )
    
    list_editable = (
        'status',
    )

    search_fields = (
        'product__title',
        'user__username',
        'subject',
        'comment'
    )

    list_filter = (
        'status',
    )

    readonly_fields = (
        'created_at',
        'updated_at',
    )

    fieldsets = (
        (None, {
            "fields": (
                'product', 'user',
                'subject', 'comment',
                'rating', 'status',
            ),
        }),
    )

# ======================= ALLOW PAYMENT ========================
@admin.register(AllowPayment)
class AllowPaymentAdmin(ModelAdmin):
    list_display = (
        'id', 'title',
        'help_time', 'image_tag', 'is_featured',
        'status', 'created_at',
        'updated_at'
    )
    
    list_editable = (
        'is_featured',
        'status',
    )

    search_fields = (
        'title',
    )

    list_filter = (
        'status',
        'is_featured'
    )

    readonly_fields = (
        'created_at',
        'updated_at',
        'image_tag',
    )

    fieldsets = (
        (None, {
            "fields": (
                'title', 'help_time',
                'image', 'is_featured', 'status',
            ),
        }),
    )