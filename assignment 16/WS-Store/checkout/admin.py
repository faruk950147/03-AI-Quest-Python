from django.contrib import admin
from checkout.models import Checkout
class CheckoutAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'profile', 'product', 'quantity', 'status', 'is_ordered', 'total_cost', 'ordered_date')
    list_editable = ('status', 'is_ordered')
admin.site.register(Checkout, CheckoutAdmin)