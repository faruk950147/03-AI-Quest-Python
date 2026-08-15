from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class SignUpForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
            
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'placeholder': 'Username'})
    )
    phone = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'placeholder': 'Phone Number'})
    )
    email = forms.EmailField(
        max_length=150,
        widget=forms.EmailInput(attrs={'placeholder': 'Email Optional'})
    )
            
    password = forms.CharField(
        max_length=150,
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'})
    )
    password2 = forms.CharField(
        max_length=150,
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'})
    )
    



class SignInForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'placeholder': 'Username or Phone or Email'})
    )
    password = forms.CharField(
        max_length=150,
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'})
    )
    

