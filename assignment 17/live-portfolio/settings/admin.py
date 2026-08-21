from django.contrib import admin
from unfold.admin import ModelAdmin

from settings.models import (
    Logo,
    Menubar,
    Footer,
    Copyright,
    SocialLink,
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
# LOGO ADMIN
# ==========================================================

@admin.register(Logo)
class LogoAdmin(SingletonAdmin):

    # ===================== LIST DISPLAY =====================
    list_display = (
        "id",
        "title",
        "status",
        "created_at",
        "updated_at",
    )

    # ===================== SEARCH =====================
    search_fields = (
        "title",
    )

    # ===================== FIELDSETS =====================
    fieldsets = (
        (
            "Logo Information",
            {
                "fields": (
                    "title",
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
# MENUBAR ADMIN
# ==========================================================

@admin.register(Menubar)
class MenubarAdmin(BaseAdmin):

    # ===================== LIST DISPLAY =====================
    list_display = (
        "id",
        "parent",
        "title",
        "url_name",
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
        "url_name",
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
            "Menu Information",
            {
                "fields": (
                    "parent",
                    "title",
                    "url_name",
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
# FOOTER ADMIN
# ==========================================================

@admin.register(Footer)
class FooterAdmin(SingletonAdmin):

    # ===================== LIST DISPLAY =====================
    list_display = (
        "id",
        "title",
        "tag",
        "paragraph",
        "status",
        "created_at",
        "updated_at",
    )

    # ===================== SEARCH =====================
    search_fields = (
        "title",
        "tag",
        "paragraph",
    )

    # ===================== FIELDSETS =====================
    fieldsets = (
        (
            "Footer Information",
            {
                "fields": (
                    "title",
                    "tag",
                    "paragraph",
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
# COPYRIGHT ADMIN
# ==========================================================

@admin.register(Copyright)
class CopyrightAdmin(SingletonAdmin):

    # ===================== LIST DISPLAY =====================
    list_display = (
        "id",
        "location",
        "designed",
        "status",
        "created_at",
        "updated_at",
    )

    # ===================== SEARCH =====================
    search_fields = (
        "location",
        "designed",
    )

    # ===================== FIELDSETS =====================
    fieldsets = (
        (
            "Copyright Information",
            {
                "fields": (
                    "location",
                    "designed",
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
# SOCIAL LINK ADMIN
# ==========================================================

@admin.register(SocialLink)
class SocialLinkAdmin(BaseAdmin):

    # ===================== LIST DISPLAY =====================
    list_display = (
        "id",
        "icon",
        "url",
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
        "icon",
        "url",
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
            "Social Link Information",
            {
                "fields": (
                    "icon",
                    "url",
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