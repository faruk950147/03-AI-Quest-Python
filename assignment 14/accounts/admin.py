from django.contrib import admin
from django.contrib.auth.models import User
from accounts.models import Profile


# Custom User Admin
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'is_staff')
    # readonly_fields = ('username', 'email', 'first_name', 'password', 'last_name', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('is_staff', 'is_superuser', 'is_active')


# Unregister default User admin
admin.site.unregister(User)
# Register custom User admin
admin.site.register(User, UserAdmin)


# Profile Admin
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user', 'name', 'division', 'district', 'thana',
        'villorroad', 'phone', 'zipcode', 'created_at', 'updated_at'
    )


# Register Profile admin
admin.site.register(Profile, ProfileAdmin)
