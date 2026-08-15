from django.contrib import admin
from .models import PhoneSearch

@admin.register(PhoneSearch)
class PhoneSearchAdmin(admin.ModelAdmin):
    # This controls which columns are visible in the admin list
    list_display = ('number', 'location', 'provider', 'latitude', 'longitude', 'created_at', 'updated_at')
    
    # This adds a search bar to find specific numbers or locations
    search_fields = ('number', 'location')
    
    # This adds a filter sidebar on the right
    list_filter = ('created_at', 'provider')