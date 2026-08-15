from django.db import models
from django.contrib.auth.models import User
from django.utils.html import mark_safe


# Create your models here.

DIVISION_CHOICES = (
    ('Dhaka', 'Dhaka'),
    ('Rangpur', 'Rangpur'),
    ('Rajshahi', 'Rajshahi'),
    ('Khulna', 'Khulna'),
    ('Barishal', 'Barishal'),
    ('Chattogram', 'Chattogram'),
    ('Mymensingh', 'Mymensingh'),
    ('Sylhet', 'Sylhet'),
)

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profile')
    name = models.CharField(max_length=200)
    division = models.CharField(choices=DIVISION_CHOICES, max_length=50)
    district = models.CharField(max_length=200)
    thana = models.CharField(max_length=100)
    villorroad = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, default='+880')
    zipcode = models.PositiveIntegerField()
    # image = models.ImageField(upload_to='Profile/%Y/%m/%d/')
    # created_date = models.DateTimeField(auto_now_add=True)
    # updated_date = models.DateTimeField(auto_now=True)
    @property
    def image_tag(self):
        try:
            return mark_safe(f'<img src="{self.image.url}" width="50" height="50"/>')
        except AttributeError:
            return mark_safe('<span>No Image</span>')

    class Meta:
        ordering = ['id']
    verbose_name_plural = '01. Profiles'

    def __str__(self):
        return f"{self.name} - {self.user.username}"

