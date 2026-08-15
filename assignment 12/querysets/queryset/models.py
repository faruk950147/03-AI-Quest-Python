from django.db import models
"""
class Manager(models.Manager):
    Custom manager for filtering active products
    
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)
    
class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    objects = Manager()
"""
class Teacher(models.Model):
    name = models.CharField(max_length=200)
    subject = models.CharField(max_length=200)
    department = models.CharField(max_length=50)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    # change manager name to teachers
    teachers = models.Manager()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "teacher"
        ordering = ["-created_at"]
        verbose_name = "Teacher"
        verbose_name_plural = "Teachers"

class Student(models.Model):

    DEPARTMENT_CHOICES = [
        ('CSE', 'Computer Science'),
        ('EEE', 'Electrical Engineering'),
        ('BBA', 'Business Administration'),
    ]

    name = models.CharField(max_length=200)
    age = models.PositiveIntegerField()
    roll = models.PositiveIntegerField(unique=True)
    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES)
    passed_in_year = models.DateField()
    passed_out_year = models.DateField()
    marks = models.DecimalField(max_digits=5, decimal_places=2)
    # change manager name to students
    students = models.Manager()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.roll} - {self.name}"

    class Meta:
        db_table = "student"
        ordering = ["-created_at"]
        verbose_name = "Student"
        verbose_name_plural = "Students"