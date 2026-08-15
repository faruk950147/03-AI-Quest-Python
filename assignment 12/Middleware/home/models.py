from django.db import models

class Student(models.Model):

    DEPARTMENT_CHOICES = [
        ('CSE', 'Computer Science'),
        ('EEE', 'Electrical Engineering'),
        ('BBA', 'Business Administration'),
    ]

    name = models.CharField(max_length=200)
    roll = models.PositiveIntegerField(unique=True)
    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES)
    passed_in_year = models.DateField()
    passed_out_year = models.DateField()

    def __str__(self):
        return f"{self.roll} - {self.name}"

    class Meta:
        ordering = ['roll']