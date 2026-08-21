from django.contrib import admin
from unfold.admin import ModelAdmin

from about.models import (
    Description,
    AboutMe,
    Stat,
    Skill,
    Interest,
    Reference,
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
# ABOUT ME ADMIN
# ==========================================================

@admin.register(AboutMe)
class AboutMeAdmin(SingletonAdmin):

    # ===================== LIST DISPLAY =====================
    list_display = (
        "id",
        "title",
        "phone",
        "email",
        "location",
        "education",
        "specialization",
        "experience",
        "availability",
        "additional",
        "description",
        "status",
        "image_tag",
        "created_at",
        "updated_at",
    )

    # ===================== SEARCH =====================
    search_fields = (
        "title",
        "phone",
        "email",
        "location",
        "education",
        "specialization",
        "experience",
        "availability",
        "github",
        "linkedin",
        "additional",
        "description",
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
            "Basic Information",
            {
                "fields": (
                    "title",
                    "phone",
                    "email",
                ),
            },
        ),
        (
            "Social Links",
            {
                "fields": (
                    "github",
                    "linkedin",
                ),
            },
        ),
        (
            "Personal Information",
            {
                "fields": (
                    "location",
                    "education",
                    "specialization",
                    "experience",
                    "availability",
                ),
            },
        ),
        (
            "Profile Image",
            {
                "fields": (
                    "image",
                    "image_tag",
                ),
            },
        ),
        (
            "Description",
            {
                "fields": (
                    "description",
                    "additional",
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
# STAT ADMIN
# ==========================================================

@admin.register(Stat)
class StatAdmin(BaseAdmin):

    # ===================== LIST DISPLAY =====================
    list_display = (
        "id",
        "icon",
        "title",
        "value",
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
    )

    # ===================== FIELDSETS =====================
    fieldsets = (
        (
            "Stat Information",
            {
                "fields": (
                    "icon",
                    "title",
                    "value",
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
# SKILL ADMIN
# ==========================================================

@admin.register(Skill)
class SkillAdmin(BaseAdmin):

    # ===================== LIST DISPLAY =====================
    list_display = (
        "id",
        "title",
        "value",
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
    )

    # ===================== FIELDSETS =====================
    fieldsets = (
        (
            "Skill Information",
            {
                "fields": (
                    "title",
                    "value",
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
# INTEREST ADMIN
# ==========================================================

@admin.register(Interest)
class InterestAdmin(BaseAdmin):

    # ===================== LIST DISPLAY =====================
    list_display = (
        "id",
        "icon",
        "title",
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
    )

    # ===================== FIELDSETS =====================
    fieldsets = (
        (
            "Interest Information",
            {
                "fields": (
                    "icon",
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
# REFERENCE ADMIN
# ==========================================================

@admin.register(Reference)
class ReferenceAdmin(BaseAdmin):

    # ===================== LIST DISPLAY =====================
    list_display = (
        "id",
        "name",
        "position",
        "company",
        "email",
        "phone",
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
        "position",
        "company",
        "email",
        "phone",
    )

    # ===================== FIELDSETS =====================
    fieldsets = (
        (
            "Reference Information",
            {
                "fields": (
                    "name",
                    "position",
                    "company",
                ),
            },
        ),
        (
            "Contact Information",
            {
                "fields": (
                    "email",
                    "phone",
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