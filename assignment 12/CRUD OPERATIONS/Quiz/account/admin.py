from django.contrib import admin
from account.models import User

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'phone', 'email', 'is_active', 'is_staff', 'is_superuser', 'date_joined', 'last_login')
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'last_login')
    search_fields = ('username', 'phone', 'email')
    ordering = ('id',)
admin.site.register(User, UserAdmin)
