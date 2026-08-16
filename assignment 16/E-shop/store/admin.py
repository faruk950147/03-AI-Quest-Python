from django.contrib import admin
from store.models import (
    Category,
    Brand,
    Product,
    Slider,
    LiveSales
)
# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'slug', 'keyword', 'description', 'image_tag', 'status', 'created_date', 'updated_date')
    prepopulated_fields = {'slug': ('title',)}
admin.site.register(Category, CategoryAdmin)

class BrandAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'slug', 'keyword', 'description', 'image_tag', 'status', 'created_date', 'updated_date')
    prepopulated_fields = {'slug': ('title',)}
admin.site.register(Brand, BrandAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'brand', 'title', 'slug', 'old_price', 'sale_price', 'available_stock', 'discount_percent', 'keyword', 'description', 'image_tag', 'status', 'created_date', 'updated_date')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('category', 'brand', 'status')
admin.site.register(Product, ProductAdmin)

class SliderAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'status', 'image_tag', 'created_date', 'updated_date')
admin.site.register(Slider, SliderAdmin)

class LiveSalesAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'subtitle', 'url', 'status', 'created_date', 'updated_date')
admin.site.register(LiveSales, LiveSalesAdmin)