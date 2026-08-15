from django.contrib import admin
from queryset.models import Teacher, Student
# Register your models here.
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'subject', 'department', 'salary', 'created_at', 'updated_at']
admin.site.register(Teacher, TeacherAdmin)

class StudentAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'age', 'roll', 'department', 'passed_in_year', 'passed_out_year', 'marks', 'created_at', 'updated_at']
admin.site.register(Student, StudentAdmin)



