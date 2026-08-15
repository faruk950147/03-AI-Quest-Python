from django.contrib import admin
from collage.models import Collage, Department
# Register your models here.
class CollageAdmin(admin.ModelAdmin):
    list_display = ('name', 'state')
admin.site.register(Collage, CollageAdmin)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'collage', 'seat', 'fees')
admin.site.register(Department, DepartmentAdmin)
