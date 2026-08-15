from django.db import models

# Create your models here.
class Batch(models.Model):
    batch = models.CharField(max_length=100)
    is_status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name = 'Batch'
        verbose_name_plural = '01 Batches'
    def __str__(self):
        return self.batch

class Student(models.Model):
    name = models.CharField(max_length=100)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    is_status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name = 'Student'
        verbose_name_plural = '02 Students' 
    def __str__(self):
        return self.name