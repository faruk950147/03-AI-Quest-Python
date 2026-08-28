from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from django.core.validators import FileExtensionValidator

from validation.validators import (
    phone_validator,
    username_validator,
    validate_image_size,
    validate_file_extension
)
from mixins.mixing import ImageTagMixin, StripMixin
from account.utils import normalize_phone_number


# ============================================================
# USER MANAGER
# ============================================================

class UserManager(BaseUserManager):
    """
    Custom manager for the custom User model.
    """

    def create_user(self, username, email, phone, password=None, **extra_fields):
        # ------------------------------------------------
        # REQUIRED FIELD VALIDATION
        # ----------------------------------------------------

        if not username:
            raise ValueError("Username is required")

        if not email:
            raise ValueError("Email is required")

        if not phone:
            raise ValueError("Phone is required")

        # ----------------------------------------------------
        # CREATE USER
        # -------------------------------------------------
        user = self.model(
            username=username,
            email=self.normalize_email(email),
            phone=normalize_phone_number(phone),
            **extra_fields,
        )

        # ----------------------------------------------------
        # PASSWORD
        # ----------------------------------------------------

        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()

        # ----------------------------------------------------
        # SAVE
        # ----------------------------------------------------

        user.save(using=self._db)

        return user

    # ========================================================
    # CREATE SUPERUSER
    # ========================================================

    def create_superuser(self, username, email, phone, password=None, **extra_fields):
        # ----------------------------------------------------
        # DEFAULT SUPERUSER VALUES
        # ----------------------------------------------------

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_verified", True)

        # ----------------------------------------------------
        # VALIDATION
        # ----------------------------------------------------

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True")

        if extra_fields.get("is_active") is not True:
            raise ValueError("Superuser must have is_active=True")

        # ----------------------------------------------------
        # CREATE SUPERUSER
        # ----------------------------------------------------

        return self.create_user(
            username=username, email=email, phone=phone, password=password, **extra_fields
        )


# ============================================================
# USER MODEL
# ============================================================

class User(StripMixin, ImageTagMixin, AbstractBaseUser, PermissionsMixin):
    """
    Custom user model.

    Authentication:
        username + password

    Additional unique identifiers:
        email
        phone
    """

    # ========================================================
    # BASIC INFORMATION
    # ========================================================

    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        validators=[
            username_validator,
        ],
    )

    email = models.EmailField(
        _("email"),
        max_length=255,
        unique=True,
    )

    phone = models.CharField(
        _("phone"),
        max_length=20,
        unique=True,
        validators=[
            phone_validator,
        ],
    )

    image = models.ImageField(
        _("image"),
        upload_to="users/%Y/%m/%d/",
        validators=[validate_image_size, validate_file_extension],
        default="defaults/default.jpg",
    )

    # ========================================================
    # ADDRESS
    # ========================================================

    country = models.CharField(
        _("country"),
        max_length=100,
        blank=True, null=True
    )

    city = models.CharField(
        _("city"),
        max_length=100,
        blank=True, null=True
    )

    home_city = models.CharField(
        _("home_city"),
        max_length=100,
        blank=True, null=True
    )

    zip_code = models.CharField(
        _("zip_code"),
        max_length=20,
        blank=True, null=True
    )

    address = models.TextField(
        _("address"),
        blank=True, null=True
    )

    # ========================================================
    # ACCOUNT STATUS
    # ========================================================

    is_active = models.BooleanField(
        _("is_active"),
        default=False,
    )

    is_staff = models.BooleanField(
        _("is_staff"),
        default=False,
    )

    is_verified = models.BooleanField(
        _("is_verified"),
        default=False,
    )

    # ========================================================
    # SYSTEM INFORMATION
    # ========================================================

    created_at = models.DateTimeField(
        _("created_at"),
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        _("updated_at"),
        auto_now=True,
    )

    # ========================================================
    # USER MANAGER
    # ========================================================

    objects = UserManager()

    # ========================================================
    # AUTHENTICATION CONFIGURATION
    # ========================================================

    USERNAME_FIELD = "username"

    REQUIRED_FIELDS = ["email", "phone"]

    # ========================================================
    # META
    # ========================================================

    class Meta:
        db_table = "account_users"

        verbose_name = "01. User"
        verbose_name_plural = "01. Users"

        ordering = ["id"]

        indexes = [models.Index(fields=["is_active", "is_verified"])]

    # ========================================================
    # CLEAN
    # ========================================================

    def clean(self):
        super().clean()

        if self.phone:
            self.phone = normalize_phone_number(self.phone)

    # ========================================================
    # SAVE
    # ========================================================
    def save(self, *args, **kwargs):
        validate = kwargs.pop("validate", True)

        if validate:
            self.full_clean()

        return super().save(*args, **kwargs)

    # ========================================================
    # STRING REPRESENTATION
    # ========================================================

    def __str__(self):
        return self.username