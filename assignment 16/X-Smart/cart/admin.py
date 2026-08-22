from django.contrib import admin
from cart.models import Cart


class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'quantity', 'paid', 'created_at', 'updated_at', 'subtotal_display')
    
    # Custom method to display subtotal
    def subtotal_display(self, obj):
        return f"{obj.product.sale_price * obj.quantity:.2f}"
    subtotal_display.short_description = "Subtotal (Tk)"
admin.site.register(Cart, CartAdmin)
