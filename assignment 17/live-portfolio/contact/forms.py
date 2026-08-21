from typing import Any
from django import forms
from django.db import transaction

from contact.models import ContactMe

# ========================= BASE STYLED FORM =========================
class StyledForm(forms.Form):
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
                field.widget.attrs.setdefault("class", "form-control")

# ========================= CONTACT FORM =========================
class ContactMeForm(StyledForm, forms.ModelForm):
    class Meta:
        model = ContactMe
        fields = ["name", "email", "subject", "message"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Your Name", "required": True}),
            "email": forms.EmailInput(attrs={"placeholder": "Your Email", "required": True}),
            "subject": forms.TextInput(attrs={"placeholder": "Subject", "required": True}),
            "message": forms.Textarea(attrs={"placeholder": "Message", "required": True}),
        }

    @transaction.atomic
    def save(self, commit: bool = True) -> ContactMe:
        contact = super().save(commit=False)
        if commit:
            contact.save()
        return contact