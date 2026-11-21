from django.contrib import admin
from student.models import Choice, Department, Question, Student


# --- Inlines ---


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 1


class StudentInline(admin.TabularInline):
    model = Student
    extra = 1


# --- Admin Registrations ---


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("id", "question_text", "pub_date")
    search_fields = ("question_text",)
    list_filter = ("pub_date",)
    ordering = ("id",)
    inlines = [ChoiceInline]


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ("id", "choice_text", "question", "votes")
    search_fields = ("choice_text", "question__question_text")
    list_filter = ("question",)
    ordering = ("id",)
    # Optimizes database performance by avoiding N+1 queries
    list_select_related = ("question",)
    # Replaces large dropdowns with searchable inputs
    autocomplete_fields = ("question",)


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)
    ordering = ("id",)
    inlines = [StudentInline]


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "department", "age")
    search_fields = ("name", "department__name")
    list_filter = ("department", "age")
    ordering = ("id",)
    # Optimizes database performance by avoiding N+1 queries
    list_select_related = ("department",)
    # Replaces large dropdowns with searchable inputs
    autocomplete_fields = ("department",)