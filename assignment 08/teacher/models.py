from django.db import models
from collage.models import Collage, Department
from django.core.validators import RegexValidator


class Teacher(models.Model):
    collage = models.ForeignKey(Collage, on_delete=models.CASCADE, related_name='teachers')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='teachers')
    name = models.CharField(max_length=150)
    email = models.EmailField(max_length=150, unique=True)
    phone = models.CharField(
        max_length=15,
        validators=[RegexValidator(regex=r'^\+?\d{10,15}$', message="Enter a valid phone number")]
    )

    def __str__(self):
        return f"Name of teacher: {self.name}"
