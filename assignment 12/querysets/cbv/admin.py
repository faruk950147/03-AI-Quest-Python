from django.contrib import admin
from cbv.models import Person

# Register your models here.
class PersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'email', 'phone', 'address', 'is_completed')
    list_filter = ('is_completed',)
    search_fields = ('name', 'email', 'phone')
    ordering = ('name',)

admin.site.register(Person, PersonAdmin)
