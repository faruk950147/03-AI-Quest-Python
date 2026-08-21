from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.html import format_html

# ======================== LOGIN/LOGOUT MIXINS ===============================
class LogoutRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse_lazy('home'))
        return super().dispatch(request, *args, **kwargs)

class LoginRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse_lazy('login'))
        return super().dispatch(request, *args, **kwargs)


# ======================== IMAGE TAG MIXIN ===============================
class ImageTagMixin:
    class Meta:
        abstract = True

    def image_tag(self):
        image = getattr(self, "image", None)

        if image and hasattr(image, "url"):
            return format_html(
                '<img src="{}" style="width:30px; height:30px; object-fit:cover; border-radius:5px; border:1px solid #ddd;" />',
                image.url,
            )

        return "No Image"

# ======================== Strip MIXIN ===============================
from django.db import models

class StripMixin:
    STRIP_FIELD_TYPES = (models.CharField, models.TextField)

    def clean(self):
        super().clean()

        for field in self._meta.fields:
            if not isinstance(field, self.STRIP_FIELD_TYPES):
                continue

            value = getattr(self, field.name, None)
            if isinstance(value, str):
                setattr(self, field.name, value.strip())