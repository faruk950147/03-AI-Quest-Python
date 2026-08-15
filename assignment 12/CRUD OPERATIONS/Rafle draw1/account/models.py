from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from account.managers import UserManager
from django.core.validators import RegexValidator

phone_validator = RegexValidator(
    r"^(\+?\d{0,4})?\s?-?\s?(\(?\d{3}\)?)\s?-?\s?(\(?\d{3}\)?)\s?-?\s?(\(?\d{4}\)?)?$",
    "The phone number provided is invalid"
)
class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        max_length=30,
        unique=True,
        validators=[UnicodeUsernameValidator()]
    )
    phone = models.CharField(
        max_length=16,
        validators=[phone_validator],
        unique=True
    )
    email = models.EmailField(
        max_length=150,
        null=True,
        blank=True,
        unique=False  # email is not unique
    )  
    is_active = models.BooleanField(default=False)  # default False 
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'  # here we set the username as the unique identifier
    REQUIRED_FIELDS = ['phone']

    def __str__(self):
        return self.username
