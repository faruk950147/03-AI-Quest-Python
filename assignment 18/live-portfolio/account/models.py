from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from django.utils.translation import gettext_lazy as _

from validation.validators import (
    phone_validator,
    username_validator,
    validate_image_size,
    validate_file_extension,
)

from mixins.mixing import ImageTagMixin, StripMixin
from account.utils import normalize_phone_number


# ==========================================================
# USER MANAGER
# ==========================================================

class UserManager(BaseUserManager):
    def create_user(self, username, email, phone, password=None, **extra_fields):
        if not username:
            raise ValueError(_("Username is required."))

        if not email:
            raise ValueError(_("Email is required."))

        if not phone:
            raise ValueError(_("Phone number is required."))

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            phone=normalize_phone_number(phone),
            **extra_fields,
        )

        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()

        # save() automatically calls full_clean()
        user.save(using=self._db)

        return user

    def create_superuser(self, username, email, phone, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_verified", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))

        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))

        return self.create_user(
            username=username,
            email=email,
            phone=phone,
            password=password,
            **extra_fields,
        )


# ==========================================================
# USER MODEL
# ==========================================================

class User(StripMixin, ImageTagMixin, AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        _("Username"),
        max_length=150,
        unique=True,
        validators=[username_validator],
        help_text=_(
            "Required. 150 characters or fewer. "
            "Letters, digits and @/./+/-/_ only."
        ),
    )

    email = models.EmailField(
        _("Email"),
        unique=True,
        help_text=_("Required. Enter a valid email address."),
    )

    phone = models.CharField(
        _("Phone"),
        max_length=15,
        unique=True,
        validators=[phone_validator],
        help_text=_("Required. Enter a valid phone number."),
    )

    image = models.ImageField(
        _("Profile Image"),
        upload_to="users/%Y/%m/%d/",
        blank=True,
        null=True,
        validators=[
            validate_file_extension,
            validate_image_size,
        ],
    )

    is_active = models.BooleanField(
        _("Active"),
        default=False,
    )

    is_staff = models.BooleanField(
        _("Staff Status"),
        default=False,
    )

    is_verified = models.BooleanField(
        _("Verified"),
        default=False,
    )

    created_at = models.DateTimeField(
        _("Created At"),
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        _("Updated At"),
        auto_now=True,
    )

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email", "phone"]

    class Meta:
        db_table = "account_users"
        verbose_name = _("01. User")
        verbose_name_plural = _("01. Users")
        ordering = ["id"]

        indexes = [
            models.Index(fields=["created_at"]),
        ]

    def clean(self):
        super().clean()

        if self.phone:
            self.phone = normalize_phone_number(self.phone)

    def save(self, *args, **kwargs):
        validate = kwargs.pop("validate", True)

        if validate:
            self.full_clean()

        return super().save(*args, **kwargs)

    def __str__(self):
        return self.username

    def __repr__(self):
        return (
            f"<User("
            f"id={self.pk}, "
            f"username={self.username!r}, "
            f"email={self.email!r}, "
            f"is_active={self.is_active}"
            f")>"
        )