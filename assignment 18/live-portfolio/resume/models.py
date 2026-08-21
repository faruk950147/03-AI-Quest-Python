from django.core.exceptions import ValidationError
from django.db import models
from ckeditor.fields import RichTextField
from django.utils.translation import gettext_lazy as _

from mixins.mixing import StripMixin
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

    description =  RichTextField(
        _("Description"),
        help_text=_("Enter the section description."),
    )

    class Meta:
        db_table = "resume_description"
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
    
class Resume(SingletonModel, StripMixin):
    title = models.CharField(
        _("Name"),
        max_length=150,
    )

    description = models.CharField(
        _("Description"),
        max_length=255,
        help_text=_("Enter a brief summary."),
    )

    location = models.CharField(
        _("Location"),
        max_length=255,
    )

    phone = models.CharField(
        _("Phone"),
        max_length=20,
    )

    email = models.EmailField(
        _("Email"),
    )

    github = models.URLField(
        _("GitHub"),
    )

    linkedin = models.URLField(
        _("LinkedIn"),
    )
    
    class Meta:
        db_table = "resume_resume"
        verbose_name = _("02 Resume")
        verbose_name_plural = _("02 Resumes")
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
        
class Education(BaseMixin, StripMixin):
    resume = models.ForeignKey(
        Resume,
        on_delete=models.CASCADE,
        related_name="educations",
    )

    qualification = models.CharField(_("Degree"), max_length=255)
    institute = models.CharField(_("Institution"), max_length=255)
    board = models.CharField(_("Board / University"), max_length=255)
    learn_start = models.DateField(_("Start Date"))
    learn_end = models.DateField(_("End Date"))

    class Meta:
        db_table = "resume_education"
        verbose_name = _("03 Education")
        verbose_name_plural = _("03 Education")
        ordering = ["id"]
            
        indexes = [
            models.Index(fields=["created_at"]),
            models.Index(fields=["status"]),
        ]
        
    def clean(self):
        super().clean()
        if self.learn_end and self.learn_start > self.learn_end:
            raise ValidationError(
                {"learn_end": "End date cannot be earlier than start date."}
            )

    def __str__(self):
        return self.resume.title

    def __repr__(self):
        return (
            f"<{self.__class__.__name__}("
            f"id={self.pk}, "
            f"status={self.status!r})>"
        )
        
class Skill(BaseMixin, StripMixin):
    resume = models.ForeignKey(
        Resume,
        on_delete=models.CASCADE,
        related_name="skills",
    )
    title = models.CharField(
        _("Title"),
        max_length=100,
    )

    typed = models.CharField(
        _("Typed Text"),
        max_length=100,
    )
        
    class Meta:
        db_table = "resume_Skill"
        verbose_name = _("04 Skills")
        verbose_name_plural = _("04 Skills")
        ordering = ["id"]
            
        indexes = [
            models.Index(fields=["created_at"]),
            models.Index(fields=["status"]),
        ]

    def __str__(self):
        return self.resume.title

    def __repr__(self):
        return (
            f"<{self.__class__.__name__}("
            f"id={self.pk}, "
            f"status={self.status!r})>"
        )

class Training(BaseMixin, StripMixin):
    resume = models.ForeignKey(
        Resume,
        on_delete=models.CASCADE,
        related_name="trainings",
    )
    title = models.CharField(
        _("Title"),
        max_length=255,
    )

    institute = models.CharField(
        _("Institute"),
        max_length=255,
    )

    learn_start = models.DateField(
        _("Start Date"),
    )

    learn_end = models.DateField(
        _("End Date"),
        blank=True,
        null=True,
    )

    description =  RichTextField(
        _("Description"),
        help_text=_("Training description."),
    )
    
    class Meta:
        db_table = "resume_training"
        verbose_name = _("05 Training")
        verbose_name_plural = _("05 Training")
        ordering = ["id"]
            
        indexes = [
            models.Index(fields=["created_at"]),
            models.Index(fields=["status"]),
        ]
        
    def clean(self):
        super().clean()
        if self.learn_end and self.learn_start > self.learn_end:
            raise ValidationError(
                {"learn_end": "End date cannot be earlier than start date."}
            )

    def __str__(self):
        return self.resume.title

    def __repr__(self):
        return (
            f"<{self.__class__.__name__}("
            f"id={self.pk}, "
            f"status={self.status!r})>"
        )

class Project(BaseMixin, StripMixin):
    resume = models.ForeignKey(
        Resume,
        on_delete=models.CASCADE,
        related_name="projects",
    )

    title = models.CharField(
        _("Project Title"),
        max_length=255,
    )

    description =  RichTextField(
        _("Description"),
        help_text=_("Project description."),
    )
    
    class Meta:
        db_table = "resume_project"
        verbose_name = _("06 Project")
        verbose_name_plural = _("06 Project")
        ordering = ["id"]
            
        indexes = [
            models.Index(fields=["created_at"]),
            models.Index(fields=["status"]),
        ]

    def __str__(self):
        return self.resume.title

    def __repr__(self):
        return (
            f"<{self.__class__.__name__}("
            f"id={self.pk}, "
            f"status={self.status!r})>"
        )

