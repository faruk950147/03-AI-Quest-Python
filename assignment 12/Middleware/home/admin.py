from django.contrib import admin
from home.models import Student
# Register your models here.

class StudentAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'roll', 'department', 'passed_in_year', 'passed_out_year']
admin.site.register(Student, StudentAdmin)

