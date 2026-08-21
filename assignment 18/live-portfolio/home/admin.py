from django.contrib import admin
from unfold.admin import ModelAdmin

from home.models import Hero


# ==========================================================
# BASE ADMIN
# ==========================================================

class BaseAdmin(ModelAdmin):

    # ===================== LIST DISPLAY =====================
    list_display = (
        "id",
        "status",
        "created_at",
        "updated_at",
    )

    # ===================== LIST EDITABLE =====================
    list_editable = (
        "status",
    )

    # ===================== SEARCH =====================
    search_fields = ()

    # ===================== FILTER =====================
    list_filter = (
        "status",
        "created_at",
        "updated_at",
    )

    # ===================== ORDER =====================
    ordering = (
        "-id",
    )

    # ===================== PAGINATION =====================
    list_per_page = 25

    # ===================== DATE =====================
    date_hierarchy = "created_at"

    # ===================== READ ONLY =====================
    readonly_fields = (
        "image_tag",
        "created_at",
        "updated_at",
    )


# ==========================================================
# SINGLETON ADMIN
# ==========================================================

class SingletonAdmin(BaseAdmin):

    # ===================== ADD PERMISSION =====================
    def has_add_permission(self, request):
        return not self.model.objects.exists()


# ==========================================================
# HERO ADMIN
# ==========================================================

@admin.register(Hero)
class HeroAdmin(SingletonAdmin):

    # ===================== LIST DISPLAY =====================
    list_display = (
        "id",
        "title",
        "tag",
        "typed_items",
        "image_tag",
        "status",
        "created_at",
        "updated_at",
    )

    # ===================== SEARCH =====================
    search_fields = (
        "title",
        "tag",
        "typed_items",
    )

    # ===================== FILTER =====================
    list_filter = (
        "status",
        "created_at",
        "updated_at",
    )

    # ===================== READ ONLY =====================
    readonly_fields = (
        "image_tag",
        "created_at",
        "updated_at",
    )

    # ===================== FIELDSETS =====================
    fieldsets = (
        (
            "Hero Information",
            {
                "fields": (
                    "title",
                    "tag",
                    "typed_items",
                ),
            },
        ),
        (
            "Hero Image",
            {
                "fields": (
                    "image",
                    "image_tag",
                ),
            },
        ),
        (
            "Status",
            {
                "fields": (
                    "status",
                ),
            },
        ),
        (
            "Important Dates",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                ),
            },
        ),
    )

