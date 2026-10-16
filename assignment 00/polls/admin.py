from django.contrib import admin
from polls.models import Choice, Question


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2
    
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("question_text", "pub_date")
    search_fields = ("question_text",)
    inlines = [ChoiceInline]
    
@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ("choice_text", "question", "votes")
    list_filter = ("question",)