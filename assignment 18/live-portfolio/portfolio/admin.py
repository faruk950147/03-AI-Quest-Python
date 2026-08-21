from django.contrib import admin
from unfold.admin import ModelAdmin

from portfolio.models import (
    Description,
    Portfolio,
    Gallery,
)


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
# DESCRIPTION ADMIN
# ==========================================================

@admin.register(Description)
class DescriptionAdmin(SingletonAdmin):

    # ===================== LIST DISPLAY =====================
    list_display = (
        "id",
        "title",
        "description",
        "status",
        "created_at",
        "updated_at",
    )

    # ===================== SEARCH =====================
    search_fields = (
        "title",
        "description",
    )

    # ===================== FIELDSETS =====================
    fieldsets = (
        (
            "Description Information",
            {
                "fields": (
                    "title",
                    "description",
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


# ==========================================================
# GALLERY INLINE
# ==========================================================

class GalleryInline(admin.StackedInline):

    model = Gallery

    extra = 1

    fields = (
        "portfolio",
        "image",
        "image_tag",
        "status",
    )

    readonly_fields = (
        "image_tag",
    )


# ==========================================================
# PORTFOLIO ADMIN
# ==========================================================

@admin.register(Portfolio)
class PortfolioAdmin(BaseAdmin):

    # ===================== LIST DISPLAY =====================
    list_display = (
        "id",
        "title",
        "types",
        "description",
        "status",
        "created_at",
        "updated_at",
    )

    # ===================== LIST EDITABLE =====================
    list_editable = (
        "types",
        "status",
    )

    # ===================== SEARCH =====================
    search_fields = (
        "title",
        "description",
    )

    # ===================== FILTER =====================
    list_filter = (
        "types",
        "status",
        "created_at",
        "updated_at",
    )

    # ===================== FIELDSETS =====================
    fieldsets = (
        (
            "Portfolio Information",
            {
                "fields": (
                    "title",
                    "types",
                    "description",
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

    # ===================== INLINE =====================
    inlines = (
        GalleryInline,
    )


# ==========================================================
# GALLERY ADMIN
# ==========================================================

@admin.register(Gallery)
class GalleryAdmin(BaseAdmin):

    # ===================== LIST DISPLAY =====================
    list_display = (
        "id",
        "portfolio",
        "image_tag",
        "status",
        "created_at",
        "updated_at",
    )

    # ===================== LIST EDITABLE =====================
    list_editable = (
        "status",
    )

    # ===================== SEARCH =====================
    search_fields = (
        "portfolio__title",
    )

    # ===================== FILTER =====================
    list_filter = (
        "status",
        "created_at",
        "updated_at",
        "portfolio__types",
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
            "Gallery Information",
            {
                "fields": (
                    "portfolio",
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
