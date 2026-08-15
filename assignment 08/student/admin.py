from django.contrib import admin
from student.models import Student
# Register your models here.
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'cgpa', 'collage', 'department')
admin.site.register(Student, StudentAdmin)