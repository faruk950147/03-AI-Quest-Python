from typing import Any

from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

from checkout.models import Shipping

class ShippingForm(forms.ModelForm):

    class Meta:
        model = Shipping
        fields = [
            'shipping_choice', 'name', 'country', 'city', 'home_city', 'zip_code', 'phone', 'address',
        ]

        widgets = {
            'shipping_choice': forms.Select(attrs={
                'class': 'form-control',
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your name',
            }),
            'country': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter country',
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter city',
            }),
            'home_city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter home city',
            }),
            'zip_code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter ZIP code',
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter phone number',
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter address',
                'rows': 4,
            }),
        }          
                
                