from django.db import models
from collage.models import Collage, Department
from django.core.validators import MinValueValidator, MaxValueValidator


class Student(models.Model):
    collage = models.ForeignKey(Collage, on_delete=models.CASCADE, related_name='students')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='students')
    name = models.CharField(max_length=150)
    email = models.EmailField(max_length=150, unique=True)
    phone = models.CharField(max_length=15)
    cgpa = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(3.50), MaxValueValidator(5.00)]
    )
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['id']
        verbose_name_plural = "Students"

    def __str__(self):
        return f"Name of student: {self.name}"
