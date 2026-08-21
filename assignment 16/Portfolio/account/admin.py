
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from unfold.admin import ModelAdmin
from account.models import User

@admin.register(User)
class UserAdmin(UserAdmin, ModelAdmin):
    list_display = (
        "id",
        "username",
        "email",
        "phone",
        "image_tag",
        "is_active",
        "is_staff",
        "is_verified",
        "is_superuser",
        "last_login",
        "created_at",
    )

    # ===================== LIST EDITABLE =====================
    list_editable = (
        "is_active",
        "is_staff",
        "is_verified",
        "is_superuser",
    )

    # ===================== SEARCH =====================
    search_fields = (
        "username",
        "email",
        "phone",
    )

    # ===================== FILTER =====================
    list_filter = (
        "is_active",
        "is_staff",
        "is_verified",
        "is_superuser",
        "created_at",
        "updated_at",
    )

    # ===================== ORDER =====================
    ordering = ("-id",)

    # ===================== PAGINATION =====================
    list_per_page = 25

    # ===================== DATE =====================
    date_hierarchy = "created_at"

    # ===================== READ ONLY =====================
    readonly_fields = (
        "image_tag",
        "last_login",
        "created_at",
        "updated_at",
    )

    # ===================== M2M =====================
    filter_horizontal = (
        "groups",
        "user_permissions",
    )

    # ===================== FIELDSETS =====================
    fieldsets = (
        (
            "Basic Information",
            {
                "fields": (
                    "username",
                    "email",
                    "phone",
                    "password",
                )
            },
        ),
        (
            "Profile",
            {
                "fields": (
                    "image",
                    "image_tag",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_verified",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (
            "Important Dates",
            {
                "fields": (
                    "last_login",
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )

    # ===================== ADD USER =====================
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "phone",
                    "password1",
                    "password2",
                ),
            },
        ),
    )