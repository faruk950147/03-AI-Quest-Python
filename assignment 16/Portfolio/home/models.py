from django.core.exceptions import ValidationError
from django.db import models
from ckeditor.fields import RichTextField
from django.utils.translation import gettext_lazy as _

from mixins.mixing import ImageTagMixin, StripMixin

from validation.validators import validate_image_size, validate_file_extension

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
# HERO MODEL
# ==========================================================
class Hero(SingletonModel, StripMixin, ImageTagMixin):
    title = models.CharField(_("Title"), max_length=200)
    tag = models.CharField(_("Tag"), max_length=200, blank=True, null=True)
    typed_items = models.CharField(
        _("Typed Items"),
        max_length=300,
        help_text=_("Comma separated values. Example: Designer, Developer, Freelancer"),
    )

    image = models.ImageField(
        _("Image"),
        upload_to="hero/%Y/%m/%d/",
        blank=True,
        null=True,
        validators=[
            validate_file_extension,
            validate_image_size,
        ],
    )

    class Meta:
        db_table = "home_hero"
        verbose_name = _("01. Hero")
        verbose_name_plural = _("01. Hero")
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
