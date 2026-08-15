from django.contrib import admin
from teacher.models import Teacher
# Register your models here.
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'collage', 'department')
admin.site.register(Teacher, TeacherAdmin)
