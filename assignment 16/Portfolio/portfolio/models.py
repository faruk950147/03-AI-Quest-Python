from django.core.exceptions import ValidationError
from django.db import models
from ckeditor.fields import RichTextField
from django.utils.translation import gettext_lazy as _
from mixins.mixing import ImageTagMixin, StripMixin
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
        _("status"),
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.ACTIVE
    )

    created_at = models.DateTimeField(
        _("created_at"),
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        _("updated_at"),
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

class Description(SingletonModel, StripMixin):
    """
    Stores the heading and description
    displayed in the About section.
    """

    title = models.CharField(
        _("title"),
        max_length=255,
        help_text=_("Enter the section title."),
    )

    description = RichTextField(
        _("description"),
        help_text=_("Enter the section description."),
    )

    class Meta:
        db_table = "portfolio_description"
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
  

class Portfolio(BaseMixin, StripMixin):
    TYPES_CHOICES = [
        ('apps', 'Apps'),
        ('webs', 'Webs'),
        ('apis', 'Apis'),
    ]

    title = models.CharField(_("title"), max_length=150)
    types = models.CharField(
        _("types"), max_length=20, choices=TYPES_CHOICES, default='apps'
    )
    live_url = models.URLField(
        _("live url"), max_length=500, blank=True, null=True, help_text="Live project URL"
    )
    description = RichTextField(_("description"), help_text="Your description")
    
    class Meta:
        db_table = "portfolio_portfolio"
        verbose_name = _("02 Portfolio")
        verbose_name_plural = _("02 Portfolio")
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


class Gallery(BaseMixin, ImageTagMixin):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name="galleries")
    image = models.FileField(_("image"), upload_to='portfolio/')
    
    class Meta:
        db_table = "portfolio_galleries"
        verbose_name = _("03 Galleries")
        verbose_name_plural = _("03 Galleries")
        ordering = ["id"]
            
        indexes = [
            models.Index(fields=["created_at"]),
            models.Index(fields=["status"]),
        ]

    def __str__(self):
        return self.portfolio.title

    def __repr__(self):
        return (
            f"<{self.__class__.__name__}("
            f"id={self.pk}, "
            f"status={self.status!r})>"
        )

