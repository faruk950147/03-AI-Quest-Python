from django import forms
from map.models import PhoneSearch
import phonenumbers
from django.core.exceptions import ValidationError

class PhoneSearchForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PhoneSearchForm, self).__init__(*args, **kwargs)
        self.fields['number'].initial = '+880'
        
    class Meta:
        model = PhoneSearch
        fields = ['number']
        widgets = {
            'number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter phone number (e.g. +88015...)',
                'id': 'number',
            }),
        }

    def clean_number(self):
        number = self.cleaned_data.get('number')

        parsed_number = phonenumbers.parse(number, None)
        
        if not phonenumbers.is_valid_number(parsed_number):
            raise ValidationError("Your number is invalid. or format code.")
        return number