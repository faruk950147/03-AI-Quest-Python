from django.contrib import admin
from unfold.admin import ModelAdmin

from service.models import Description, Service


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
            "Basic Information",
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
# SERVICE ADMIN
# ==========================================================

@admin.register(Service)
class ServiceAdmin(BaseAdmin):

    # ===================== LIST DISPLAY =====================
    list_display = (
        "id",
        "icon",
        "title",
        "additional",
        "description",
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
        "title",
        "icon",
        "additional",
        "description",
    )

    # ===================== FILTER =====================
    list_filter = (
        "status",
        "created_at",
        "updated_at",
    )

    # ===================== FIELDSETS =====================
    fieldsets = (
        (
            "Service Information",
            {
                "fields": (
                    "icon",
                    "title",
                ),
            },
        ),
        (
            "Additional Information",
            {
                "fields": (
                    "additional",
                ),
            },
        ),
        (
            "Service Description",
            {
                "fields": (
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
