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


# ==========================================================
# CONTACT MODEL
# ==========================================================
class Description(BaseMixin, StripMixin):
    title = models.CharField(_("title"), max_length=200)
    description = RichTextField(_("description"), help_text="Description")
    
    class Meta:
        db_table = "description"
        verbose_name = _("01. Description")
        verbose_name_plural = _("01. Descriptions")
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

class ContactInfo(BaseMixin, StripMixin):
    icon = models.CharField(_("icon"), max_length=100, blank=True, null=True)
    title = models.CharField(_("title"), max_length=100, blank=True, null=True)
    location = models.CharField(_("location"), max_length=200, blank=True, null=True)
    phone = models.CharField(_("phone"), max_length=30, blank=True, null=True)
    email = models.EmailField(_("email"), blank=True, null=True)

    class Meta:
        db_table = "contact_info"
        verbose_name = _("02. Contact Info")
        verbose_name_plural = _("02. Contact Infos")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.email} - {self.location}"
    
class ContactMe(BaseMixin, StripMixin):
    name = models.CharField(_("name"), max_length=100)
    email = models.EmailField(_("email"), help_text="Your Email")
    subject = models.CharField(_("subject"), max_length=200)
    message = models.TextField(_("message"), help_text="Your Messages")
    
    class Meta:
        db_table = "contact_me"
        verbose_name = _("03. Contact Me")
        verbose_name_plural = _("03. Contact Mes")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} - {self.subject}"