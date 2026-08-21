from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from unfold.admin import ModelAdmin

from account.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):

    # =========================================================
    # LIST DISPLAY
    # =========================================================
    list_display = (
        "id",
        "username",
        "email",
        "phone",
        "image_tag",
        "country",
        "city",
        "home_city",
        "zip_code",
        "address",
        "is_active",
        "is_staff",
        "is_superuser",
        "is_verified",
        "created_at",
        "updated_at",
    )

    # =========================================================
    # LIST EDITABLE
    # =========================================================
    list_editable = (
        "is_active",
        "is_staff",
        "is_superuser",
        "is_verified",
    )

    # =========================================================
    # LIST FILTER
    # =========================================================
    list_filter = (
        "is_verified",
        "is_active",
        "is_staff",
        "is_superuser",
        "created_at",
        "updated_at",
    )

    # =========================================================
    # SEARCH
    # =========================================================
    search_fields = (
        "username",
        "email",
        "phone",
        "country",
        "city",
        "home_city",
        "zip_code",
        "address",
    )

    # =========================================================
    # ORDERING
    # =========================================================
    ordering = (
        "id",
    )

    # =========================================================
    # FILTER HORIZONTAL
    # =========================================================
    filter_horizontal = (
        "groups",
        "user_permissions",
    )

    # =========================================================
    # READ ONLY
    # =========================================================
    readonly_fields = (
        "image_tag",
        "last_login",
        "created_at",
        "updated_at",
    )

    # =========================================================
    # FIELDSETS
    # =========================================================
    fieldsets = (

        # -----------------------------------------------------
        # BASIC INFO
        # -----------------------------------------------------
        (
            "Basic Info",
            {
                "fields": (
                    "username",
                    "email",
                    "phone",
                    "password",
                )
            }
        ),

        # -----------------------------------------------------
        # PROFILE INFO
        # -----------------------------------------------------
        (
            "Profile Info",
            {
                "fields": (
                    "image",
                    "image_tag",
                    "country",
                    "city",
                    "home_city",
                    "zip_code",
                    "address",
                )
            }
        ),

        # -----------------------------------------------------
        # PERMISSIONS
        # -----------------------------------------------------
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "is_verified",
                    "groups",
                    "user_permissions",
                )
            }
        ),

        # -----------------------------------------------------
        # ACTIVITY
        # -----------------------------------------------------
        (
            "Activity",
            {
                "fields": (
                    "last_login",
                )
            }
        ),

        # -----------------------------------------------------
        # TIMESTAMPS
        # -----------------------------------------------------
        (
            "Timestamps",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            }
        ),
    )

    # =========================================================
    # ADD USER
    # =========================================================
    add_fieldsets = (
        (
            "Basic Info",
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