from django.contrib import admin
from task.models import Task

# Register your models here.
class TaskAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'name', 'department', 'phone', 'is_completed'
    ]
admin.site.register(Task, TaskAdmin)