from datetime import date

from django.core.exceptions import ValidationError
from django.db import models
from ckeditor.fields import RichTextField
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator
from django.core.validators import MinValueValidator

from mixins.mixing import ImageTagMixin, StripMixin
from validation.validators import (
    phone_validator,
    validate_file_extension,
    validate_image_size,
)

# ==========================================================
# STATUS CHOICES
# ==========================================================
class StatusChoices(models.TextChoices):
    ACTIVE = "active", _("Active")
    INACTIVE = "inactive", _("Inactive")


# ==========================================================
# BASE MODEL
# ==========================================================
class BaseMixin(models.Model):
    """
    Abstract base model containing common fields.
    """

    status = models.CharField(
        _("Status"),
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.ACTIVE
    )

    created_at = models.DateTimeField(
        _("Created At"),
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        _("Updated At"),
        auto_now=True,
    )

    class Meta:
        abstract = True


# ==========================================================
# SINGLETON MODEL
# ==========================================================
class SingletonModel(BaseMixin):
    """
    Abstract model that allows only one database record.
    """

    class Meta:
        abstract = True

    def clean(self):
        super().clean()

        if self.__class__.objects.exclude(pk=self.pk).exists():
            raise ValidationError(
                _("Only one %(model)s instance is allowed."),
                params={"model": self._meta.verbose_name},
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)


# ==========================================================
# DESCRIPTION MODEL
# ==========================================================

class Description(SingletonModel, StripMixin):
    """
    Stores the heading and description
    displayed in the About section.
    """

    title = models.CharField(
        _("Title"),
        max_length=255,
        help_text=_("Enter the section title."),
    )

    description = RichTextField(
        _("Description"),
        help_text=_("Enter the section description."),
    )

    class Meta:
        db_table = "about_description"
        verbose_name = _("01. Description")
        verbose_name_plural = _("01. Description")
        ordering = ["id"]
        
        indexes = [
            models.Index(fields=["title"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["status"]),
        ]

    def __str__(self):
        return self.title

    def __repr__(self):
        return (
            f"<{self.__class__.__name__}("
            f"id={self.pk}, "
            f"status={self.status!r})>"
        )

class AboutMe(SingletonModel, ImageTagMixin, StripMixin):
    """
    Stores the personal information displayed on the About section.
    """

    title = models.CharField(
        _("Title"), max_length=100, help_text=_("Enter the title for the About Me section.")
    )
    phone = models.CharField( 
        _("Phone"), max_length=20, blank=True, null=True, help_text=_("Valid Phone number"),
        validators=[phone_validator],
    )
    email = models.EmailField(
        _("Email"), help_text=_("Valid email")
    )
    github = models.URLField(
        _("Github"), blank=True, null=True, help_text=_("Github url")
    )
    linkedin = models.URLField(
        _("LinkedIn"), blank=True, null=True, help_text=_("LinkedIn url")
    )
    location = models.CharField(
        _("Location"), max_length=100, blank=True, null=True, help_text=_("Your location")
    )
    education = models.CharField(
        _("Education"), max_length=100, blank=True, null=True, help_text=_("Your education")
    )
    specialization = models.CharField(
        _("Specialization"), max_length=100, blank=True, null=True, help_text=_("Your specialization")
    )
    experience = models.CharField(
        _("Experience"), max_length=100, blank=True, null=True, help_text=_("Your experience")
    )
    availability = models.CharField(
        _("Availability"), max_length=100, blank=True, null=True, help_text=_("Your availability")
    )
    image = models.ImageField(
        _("Profile Image"),
        upload_to="about/",
        validators=[
            validate_file_extension,
            validate_image_size,
        ],
    )
    additional = RichTextField(_("Additional Description"), help_text=_("Additional description"))
    description = RichTextField(_("Description"), help_text=_("Description about you"))
    
    class Meta:
        db_table = "about_me"
        verbose_name = _("02. About Me")
        verbose_name_plural = _("02. About Me")
        ordering = ["id"]
        
        indexes = [
            models.Index(fields=["created_at"]),
            models.Index(fields=["status"]),
        ]

    def __str__(self):
        return self.title

    def __repr__(self):
        return (
            f"<{self.__class__.__name__}("
            f"id={self.pk}, "
            f"status={self.status!r})>"
        )
    
class Stat(BaseMixin, StripMixin):
    """
    Stores the statistics displayed on the About section.
    """
    icon = models.CharField(_("Icon"), max_length=100, blank=True, null=True, help_text=_("Enter the icon class for the stat."))
    title = models.CharField(_("Title"), max_length=100, help_text=_("Enter the stat title."))
    value = models.PositiveIntegerField(
        _("Value"), default=0, help_text=_("Enter the stat value as a number."),
        validators=[
            MinValueValidator(0, message=_("Value must be at least 0.")),
            MaxValueValidator(100000, message=_("Value cannot exceed 100000."))
        ],
    )

    class Meta:
        db_table = "about_stats"
        verbose_name = _("03. Stats")
        verbose_name_plural = _("03. Stats")
        ordering = ["id"]
        
        indexes = [
            models.Index(fields=["created_at"]),
            models.Index(fields=["status"]),
        ]

    def __str__(self):
        return f"{self.title}: {self.value}"
    
    def __repr__(self):
        return (
            f"<{self.__class__.__name__}("
            f"id={self.pk}, "
            f"status={self.status!r})>"
        )
        
class Skill(BaseMixin, StripMixin):
    title = models.CharField(_("Title"), max_length=100, help_text=_("Enter the skill title."))
    value = models.PositiveIntegerField(
        _("Value"),
        help_text=_("Enter the skill value as a percentage (0-100)."),
        validators=[
            MinValueValidator(0, message=_("Value must be at least 0.")),
            MaxValueValidator(100, message=_("Value cannot exceed 100.")),
        ],
    )

    class Meta:
        db_table = "about_skills"
        verbose_name = _("04. Skills")
        verbose_name_plural = _("04. Skills")
        ordering = ["id"]
        indexes = [
            models.Index(fields=["created_at"]),
            models.Index(fields=["status"]),
        ]
    
    def __str__(self):
        return f"{self.title}: {self.value}"
    
    def __repr__(self):
        return (
            f"<{self.__class__.__name__}("
            f"id={self.pk}, "
            f"status={self.status!r})>"
        )

class Interest(BaseMixin, StripMixin):
    icon = models.CharField(_("Icon"), max_length=100, blank=True, null=True, help_text=_("Enter the icon class for the interest."))
    title = models.CharField(_("Title"), max_length=100, help_text=_("Enter the interest title."))

    class Meta:
        db_table = "about_interests"
        verbose_name = _("05. Interests")
        verbose_name_plural = _("05. Interests")
        ordering = ["id"]
        
        indexes = [
            models.Index(fields=["created_at"]),
            models.Index(fields=["status"]),
        ]

    def __str__(self):
        return self.title

    def __repr__(self):
        return (
            f"<{self.__class__.__name__}("
            f"id={self.pk}, "
            f"status={self.status!r})>"
        )

class Reference(BaseMixin, StripMixin):
    """
    Stores the references/testimonials displayed on the About section.
    """
    name = models.CharField(_("Name"), max_length=100, help_text=_("Enter the reference's name."))
    position = models.CharField(_("Position"), max_length=100, blank=True, null=True, help_text=_("Enter the reference's position."))
    company = models.CharField(_("Company"), max_length=100, blank=True, null=True, help_text=_("Enter the reference's company."))
    email = models.EmailField(_("Email"), blank=True, null=True, help_text=_("Enter the reference's email."))
    phone = models.CharField(_("Phone"), max_length=20, blank=True, null=True, validators=[phone_validator], help_text=_("Enter the reference's phone number."))

    class Meta:
        db_table = "about_references"
        verbose_name = _("06. References")
        verbose_name_plural = _("06. References")
        ordering = ["id"]
        
        indexes = [
            models.Index(fields=["created_at"]),
            models.Index(fields=["status"]),
        ]

    def __str__(self):
        return self.name
    
    def __repr__(self):
        return (
            f"<{self.__class__.__name__}("
            f"id={self.pk}, "
            f"status={self.status!r})>"
        )