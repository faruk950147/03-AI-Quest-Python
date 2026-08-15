from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Person(models.Model):
    name = models.CharField(max_length=100, verbose_name="Full Name", help_text="Enter your full name")
    age = models.IntegerField(default=18, validators=[MinValueValidator(0), MaxValueValidator(120)])
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "person"
        ordering = ["-created_at"]
        verbose_name = "Person"
        verbose_name_plural = "People"

    def __str__(self):
        return self.name