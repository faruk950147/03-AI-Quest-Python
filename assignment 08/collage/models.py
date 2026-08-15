from django.db import models
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import MinValueValidator, MaxValueValidator


class Collage(models.Model):
    name = models.CharField(validators=[UnicodeUsernameValidator()], max_length=200)  
    state = models.TextField()
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['id']
        verbose_name_plural = "Collages"

    def __str__(self):
        return f"Name of collage: {self.name}"


class Department(models.Model):
    collage = models.ForeignKey(Collage, on_delete=models.CASCADE, related_name='departments')  # নামটা অর্থপূর্ণ করা ভালো
    name = models.CharField(validators=[UnicodeUsernameValidator()], max_length=200)
    seat = models.IntegerField(validators=[MinValueValidator(5), MaxValueValidator(120)], default=5)
    fees = models.DecimalField(max_digits=10, decimal_places=2, default=650000)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['id']
        verbose_name_plural = "Departments"

    def __str__(self):
        return f"Name of department: {self.name}"
