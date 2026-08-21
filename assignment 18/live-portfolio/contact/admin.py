from django.contrib import admin
from unfold.admin import ModelAdmin

from contact.models import (
    Description,
    ContactInfo,
    ContactMe,
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
# CONTACT INFO ADMIN
# ==========================================================

@admin.register(ContactInfo)
class ContactInfoAdmin(BaseAdmin):

    # ===================== LIST DISPLAY =====================
    list_display = (
        "id",
        "icon",
        "title",
        "location",
        "phone",
        "email",
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
        "location",
        "phone",
        "email",
    )

    # ===================== FIELDSETS =====================
    fieldsets = (
        (
            "Contact Information",
            {
                "fields": (
                    "icon",
                    "title",
                    "location",
                    "phone",
                    "email",
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
# CONTACT ME ADMIN
# ==========================================================

@admin.register(ContactMe)
class ContactMeAdmin(BaseAdmin):

    # ===================== LIST DISPLAY =====================
    list_display = (
        "id",
        "name",
        "email",
        "subject",
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
        "name",
        "email",
        "subject",
        "message",
    )

    # ===================== FIELDSETS =====================
    fieldsets = (
        (
            "Sender Information",
            {
                "fields": (
                    "name",
                    "email",
                ),
            },
        ),
        (
            "Message Information",
            {
                "fields": (
                    "subject",
                    "message",
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
