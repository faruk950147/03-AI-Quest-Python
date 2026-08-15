from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.html import mark_safe
from django.dispatch import receiver
from django.db.models.signals import post_save

# Manager for custom user model
class Manager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError("Username must be set")
        if not email:
            raise ValueError("Email must be set")

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        # Automatically create Shipping for this user without signal
        # Shipping.objects.create(user=user)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        return self.create_user(username, email, password, **extra_fields)


# Custom user model
class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[UnicodeUsernameValidator()]
    )
    email = models.EmailField(max_length=150, unique=True)

    image = models.ImageField(upload_to='user/', default='defaults/default.jpg')

    country = models.CharField(max_length=150, blank=True, null=True)
    city = models.CharField(max_length=150, blank=True, null=True)
    home_city = models.CharField(max_length=150, blank=True, null=True)
    zip_code = models.CharField(max_length=15, blank=True, null=True)
    phone = models.CharField(max_length=16, blank=True, null=True)
    address = models.TextField(max_length=500, blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = Manager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    class Meta:
        ordering = ['id']
        verbose_name_plural = "01. Users"

    def __str__(self):
        return self.username

    @property
    def image_tag(self):
        if self.image:
            return mark_safe(f'<img src="{self.image.url}" width="40"/>')
        return "No Image"


# Shipping information model
class Shipping(models.Model):
    SHIPPING_CHOICES = (('Home', 'Home'), ('Office', 'Office'))
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shipping'
    )
    shipping_choice = models.CharField(max_length=20, choices=SHIPPING_CHOICES, default='Home')
    name = models.CharField(max_length=150, blank=True, null=True)
    country = models.CharField(max_length=150, blank=True, null=True)
    city = models.CharField(max_length=150, blank=True, null=True)
    home_city = models.CharField(max_length=150, blank=True, null=True)
    zip_code = models.CharField(max_length=15, blank=True, null=True)
    phone = models.CharField(max_length=16, blank=True, null=True)
    address = models.TextField(max_length=500, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['id']
        verbose_name_plural = "02. Shipping"

    def __str__(self):
        return f"{self.user.username} Shipping"


# Signal to create Shipping instance when a User is created
@receiver(post_save, sender=User)
def create_shipping(sender, instance, created, **kwargs):
    if created:
        Shipping.objects.create(user=instance)

