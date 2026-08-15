from django.contrib import admin
from student.models import Student, Batch
# Register your models here.


class BatchAdmin(admin.ModelAdmin):
    list_display = ('id', 'batch', 'is_status', 'created_at', 'updated_at')
admin.site.register(Batch, BatchAdmin)

class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'batch', 'is_status', 'created_at', 'updated_at')
admin.site.register(Student, StudentAdmin)
