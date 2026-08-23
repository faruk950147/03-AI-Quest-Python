from django.core.exceptions import ValidationError
from django.db import models
from ckeditor.fields import RichTextField
from django.urls import reverse
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
# LOGO
# ==========================================================
class Logo(SingletonModel):
    title = models.CharField(
        _("title"),
        max_length=100,
    )

    class Meta:
        db_table = "settings_logo"
        verbose_name = _("01. Logo")
        verbose_name_plural = _("01. Logo")
        ordering = ["id"]

    def __str__(self):
        return self.title


# ==========================================================
# MENUBAR
# ==========================================================
class Menubar(BaseMixin):
    parent = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="children",
    )
    
    title = models.CharField(
        _("title"),
        max_length=100,
    )
    url_name = models.CharField(_("url_name"), max_length=100, null=True, blank=True)

    def get_url(self):
        if self.url_name:
            return reverse(self.url_name)
        return "#"
    
    class Meta:
        db_table = "settings_menubar"
        verbose_name = _("02. Menubar")
        verbose_name_plural = _("02. Menubar")
        ordering = ["id"]

    def __str__(self):
        return self.title


# ==========================================================
# FOOTER
# ==========================================================
class Footer(SingletonModel):
    title = models.CharField(
        _("title"),
        max_length=100,
    )
    
    tag = models.CharField(
        _("tag"),
        max_length=250
    )
    
    paragraph =  RichTextField(
        _("paragraph"),
        blank=True,
        null=True,
    )

    class Meta:
        db_table = "settings_footer"
        verbose_name = _("03. Footer")
        verbose_name_plural = _("03. Footer")
        ordering = ["id"]
        
    def __str__(self):
        return self.title


# ==========================================================
# COPYRIGHT
# ==========================================================
class Copyright(SingletonModel):
    location = models.CharField(
        _("location"),
        max_length=150,
    )

    designed = models.CharField(
        _("designed"),
        max_length=150,
    )

    class Meta:
        db_table = "settings_copyright"
        verbose_name = _("04. Copyright")
        verbose_name_plural = _("04. Copyright")
        ordering = ["id"]

    def __str__(self):
        return self.designed


# ==========================================================
# SOCIAL LINK
# ==========================================================
class SocialLink(BaseMixin):
    icon = models.CharField(
        _("icon"),
        max_length=100,
        help_text=_("Example: fa-brands fa-facebook"),
    )

    url = models.URLField(_("url"))

    class Meta:
        db_table = "settings_socialLink"
        verbose_name = _("05. SocialLink")
        verbose_name_plural = _("05. SocialLink")
        ordering = ["id"]
        
    def __str__(self):
        return self.url