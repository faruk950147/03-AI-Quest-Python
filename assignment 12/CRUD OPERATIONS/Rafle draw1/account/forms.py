from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class SignUpForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
            
    password = forms.CharField(
        max_length=150,
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'})
    )
    password2 = forms.CharField(
        max_length=150,
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'})
    )

    class Meta:
        model = User
        fields = (
            'username', 'phone', 'email', 'password', 'password2',
        )
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Phone Number'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
        }
        

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
    

class ResetPasswordForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})

    email = forms.EmailField(
        max_length=150,
        widget=forms.EmailInput(attrs={'placeholder': 'Email'})
    )


class ResetPasswordConfirmForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})

    password = forms.CharField(
        max_length=150,
        widget=forms.PasswordInput(attrs={'placeholder': 'New Password'})
    )
    password2 = forms.CharField(
        max_length=150,
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'})
    )


class ChangePasswordForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})
    
    current_password = forms.CharField(
        max_length=150,
        widget=forms.PasswordInput(attrs={'placeholder': 'Current Password'})
    )
    password = forms.CharField(
        max_length=150,
        widget=forms.PasswordInput(attrs={'placeholder': 'New Password'})
    )
    password2 = forms.CharField(
        max_length=150,
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'})
    )
