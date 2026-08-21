from django.contrib import admin
from unfold.admin import ModelAdmin

from resume.models import (
    Description,
    Resume,
    Education,
    Skill,
    Training,
    Project,
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
# RESUME ADMIN
# ==========================================================

@admin.register(Resume)
class ResumeAdmin(SingletonAdmin):

    # ===================== LIST DISPLAY =====================
    list_display = (
        "id",
        "title",
        "email",
        "phone",
        "description",
        "location",
        "status",
        "created_at",
        "updated_at",
    )

    # ===================== SEARCH =====================
    search_fields = (
        "title",
        "email",
        "phone",
        "location",
        "github",
        "linkedin",
        "description",
    )

    # ===================== FIELDSETS =====================
    fieldsets = (
        (
            "Personal Information",
            {
                "fields": (
                    "title",
                    "description",
                    "location",
                ),
            },
        ),
        (
            "Contact Information",
            {
                "fields": (
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
# EDUCATION ADMIN
# ==========================================================

@admin.register(Education)
class EducationAdmin(BaseAdmin):

    # ===================== LIST DISPLAY =====================
    list_display = (
        "id",
        "qualification",
        "institute",
        "board",
        "learn_start",
        "learn_end",
        "resume",
        "status",
        "created_at",
        "updated_at",
    )

    # ===================== SEARCH =====================
    search_fields = (
        "qualification",
        "institute",
        "board",
        "resume__title",
    )

    # ===================== FILTER =====================
    list_filter = (
        "status",
        "board",
        "learn_start",
        "learn_end",
        "created_at",
        "updated_at",
    )

    # ===================== AUTOCOMPLETE =====================
    autocomplete_fields = (
        "resume",
    )

    # ===================== FIELDSETS =====================
    fieldsets = (
        (
            "Education Information",
            {
                "fields": (
                    "resume",
                    "qualification",
                    "institute",
                    "board",
                ),
            },
        ),
        (
            "Education Period",
            {
                "fields": (
                    "learn_start",
                    "learn_end",
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
        "typed",
        "resume",
        "status",
        "created_at",
        "updated_at",
    )

    # ===================== SEARCH =====================
    search_fields = (
        "title",
        "typed",
        "resume__title",
    )

    # ===================== FILTER =====================
    list_filter = (
        "status",
        "typed",
        "created_at",
        "updated_at",
    )

    # ===================== AUTOCOMPLETE =====================
    autocomplete_fields = (
        "resume",
    )

    # ===================== FIELDSETS =====================
    fieldsets = (
        (
            "Skill Information",
            {
                "fields": (
                    "resume",
                    "title",
                    "typed",
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
# TRAINING ADMIN
# ==========================================================

@admin.register(Training)
class TrainingAdmin(BaseAdmin):

    # ===================== LIST DISPLAY =====================
    list_display = (
        "id",
        "title",
        "institute",
        "learn_start",
        "learn_end",
        "description",
        "resume",
        "status",
        "created_at",
        "updated_at",
    )

    # ===================== SEARCH =====================
    search_fields = (
        "title",
        "institute",
        "description",
        "resume__title",
    )

    # ===================== FILTER =====================
    list_filter = (
        "status",
        "learn_start",
        "learn_end",
        "created_at",
        "updated_at",
    )

    # ===================== AUTOCOMPLETE =====================
    autocomplete_fields = (
        "resume",
    )

    # ===================== FIELDSETS =====================
    fieldsets = (
        (
            "Training Information",
            {
                "fields": (
                    "resume",
                    "title",
                    "institute",
                ),
            },
        ),
        (
            "Training Period",
            {
                "fields": (
                    "learn_start",
                    "learn_end",
                ),
            },
        ),
        (
            "Description",
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


# ==========================================================
# PROJECT ADMIN
# ==========================================================

@admin.register(Project)
class ProjectAdmin(BaseAdmin):

    # ===================== LIST DISPLAY =====================
    list_display = (
        "id",
        "title",
        "description",
        "resume",
        "status",
        "created_at",
        "updated_at",
    )

    # ===================== SEARCH =====================
    search_fields = (
        "title",
        "description",
        "resume__title",
    )

    # ===================== FILTER =====================
    list_filter = (
        "status",
        "created_at",
        "updated_at",
    )

    # ===================== AUTOCOMPLETE =====================
    autocomplete_fields = (
        "resume",
    )

    # ===================== FIELDSETS =====================
    fieldsets = (
        (
            "Project Information",
            {
                "fields": (
                    "resume",
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
