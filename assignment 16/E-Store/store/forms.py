from typing import Any
from django import forms
from django.contrib.auth import (
    get_user_model,
)
User = get_user_model()

from store.models import Review

# ============================================================
# BASE STYLED FORM
# ============================================================

class StyledForm(forms.Form):
    """
    Base form for consistent Bootstrap styling.
    """
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(
                field.widget,
                (
                    forms.TextInput,
                    forms.PasswordInput,
                    forms.EmailInput,
                    forms.NumberInput,
                    forms.Textarea,
                ),
            ):
                field.widget.attrs.setdefault(
                    "class",
                    "form-control",
                )

class ReviewForm(StyledForm, forms.ModelForm):
    class Meta:
        model = Review
        fields = ("subject", "comment", "rating")
        widgets = {
            "subject": forms.TextInput(attrs={"placeholder": "Review title"}),
            "comment": forms.Textarea(
                attrs={"rows": 4, "placeholder": "Write your review..."}
            ),
            "rating": forms.NumberInput(attrs={"min": 1, "max": 5}),
        }
    def clean(self):
        cleaned_data = super().clean()

        subject = cleaned_data.get("subject")
        comment = cleaned_data.get("comment")

        if not subject:
            raise forms.ValidationError("Subject is required.")

        if not comment:
            raise forms.ValidationError("Comment is required.")

        return cleaned_data