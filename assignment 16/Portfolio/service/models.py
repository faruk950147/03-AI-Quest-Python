from django.core.exceptions import ValidationError
from django.db import models
from ckeditor.fields import RichTextField
from django.utils.translation import gettext_lazy as _

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
class Description(SingletonModel):
    title = models.CharField(
        _("Title"),
        max_length=100,
    )
    description =  RichTextField(
        _("Description"),
        help_text=_("Describe your service."),
    )

    class Meta:
        db_table = "services_description"
        verbose_name = _("01. Description")
        verbose_name_plural = _("01. Description")
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


# ==========================================================
class Service(BaseMixin):
    icon = models.CharField(
        _("Icon"),
        max_length=50,
        help_text=_("Bootstrap Icon. Example: bi bi-code-slash"),
    )

    title = models.CharField(
        _("Title"),
        max_length=100,
    )

    additional =  RichTextField(
        _("Additional Description"),
        help_text=_("Additional description."),
    )

    description =  RichTextField(
        _("Description"),
        help_text=_("Describe your service."),
    )

    class Meta:
        db_table = "services_service"
        verbose_name = _("01. Services")
        verbose_name_plural = _("01. Services")
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
    