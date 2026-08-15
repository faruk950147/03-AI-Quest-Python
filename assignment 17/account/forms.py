import threading
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from account.models import Shipping
User = get_user_model()


""" 
SignUp form
"""
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
        fields = ('username', 'email', 'password', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
        }
        
    def clean_username(self):
        username = self.cleaned_data.get("username")

        if not username:
            raise ValidationError("Username is required")

        # Check if it's a string and alphanumeric
        if not username.isalnum():
            raise ValidationError("Username should only contain letters and numbers")

        # Check if username already exists
        if User.objects.filter(username__iexact=username).exists():
            raise ValidationError("Username is already taken")

        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError("Email is already registered")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if not password:
            raise ValidationError("Password is required")

        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long")

        if password != password2:
            raise ValidationError("Passwords do not match")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])  # hashed password save
        if commit:
            user.save()
        return user        
""" 
SignIn form
"""
class SignInForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'placeholder': 'Username or Email'})
    )
    password = forms.CharField(
        max_length=150,
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'})
    )
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        user = authenticate(username=username, password=password)
        if not user:
            raise ValidationError("Invalid username or password")

        cleaned_data['user'] = user
        return cleaned_data

""" 
Change password confirm form
"""     
class ChangePasswordForm(forms.Form):
    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
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

    # Validate current password
    def clean_current_password(self):
        current_password = self.cleaned_data.get('current_password')
        if self.user and not self.user.check_password(current_password):
            raise ValidationError("Current password is incorrect")
        return current_password

    # Validate new password & confirm password
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password:
            if len(password) < 8:
                self.add_error('password', "New password must be at least 8 characters long")

            if password != password2:
                self.add_error('password2', "Passwords do not match")

        return cleaned_data

""" 
Reset password form
"""    
class ResetPasswordForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})

    email = forms.EmailField(
        max_length=150,
        widget=forms.EmailInput(attrs={'placeholder': 'Email'})
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if not User.objects.filter(email__iexact=email).exists():
            raise ValidationError("No account found with this email")

        return email

""" 
Reset password confirm form
"""
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

    # clean method for multi-field validation
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if not password:
            raise ValidationError("Password is required")

        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long")

        if password != password2:
            raise ValidationError("Passwords do not match")

        return cleaned_data

""" 
User Form
"""
class UserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
               
    class Meta:
        model = User
        fields = (
            'username', 'email', 'image', 'country', 'city', 'home_city', 'zip_code', 'phone', 'address',
        )
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
            'country': forms.TextInput(attrs={'placeholder': 'Country'}),
            'city': forms.TextInput(attrs={'placeholder': 'City'}),
            'home_city': forms.TextInput(attrs={'placeholder': 'Home City'}),
            'zip_code': forms.TextInput(attrs={'placeholder': 'Zip Code'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Phone'}),
            'address': forms.Textarea(attrs={'placeholder': 'Address', 'rows': 3}),
        }


""" 
Shipping Form
"""
class ShippingForm(forms.ModelForm):
            
    class Meta:
        model = Shipping
        fields = (
            'shipping_choice', 'name', 'country', 'city', 'home_city', 'zip_code', 'phone', 'address',
        )
        widgets = {
            'shipping_choice': forms.RadioSelect(attrs={'class': 'form-check-input'}),
            'name': forms.TextInput(attrs={'placeholder': 'Name', 'class': 'form-control'}),
            'country': forms.TextInput(attrs={'placeholder': 'Country', 'class': 'form-control'}),
            'city': forms.TextInput(attrs={'placeholder': 'City', 'class': 'form-control'}),
            'home_city': forms.TextInput(attrs={'placeholder': 'Home City', 'class': 'form-control'}),
            'zip_code': forms.TextInput(attrs={'placeholder': 'Zip Code', 'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Phone', 'class': 'form-control'}),
            'address': forms.Textarea(attrs={'placeholder': 'Address', 'rows': 3, 'class': 'form-control'}),
        }
     