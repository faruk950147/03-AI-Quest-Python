from django import forms
from django.contrib.auth import get_user_model
User = get_user_model()
# why use gettext_lazy as _ ? because it's for translation purpose
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import password_validation
from django.contrib.auth.forms import (
    UserCreationForm, 
    AuthenticationForm,
    PasswordChangeForm,  # it's with old password
    SetPasswordForm,   # it's without old password
    PasswordResetForm
)
from accounts.models import Profile
# SignUpForm
class SignUpForm(UserCreationForm):
    username = forms.CharField(label=_('Username'), max_length=150, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    email = forms.EmailField(label=_('Email'), widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    password1 = forms.CharField(label=_('Password'), widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    password2 = forms.CharField(label=_('Confirm Password'), widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(_('Username already exists'))
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(_('Email already exists'))
        return email

    def save(self, commit=True):
        # save() method of UserCreationForm is overridden to save email field
        # because by default UserCreationForm does not handle email field
        # So we need to override save method to save email field
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

# SignInForm
class SignInForm(AuthenticationForm):
    username = forms.CharField(label='Username', max_length=150, widget=forms.TextInput(attrs={'autofocus':True, 'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(label=_('Password'),strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'current_password','class':'form-control' }))

    
    class Meta:
        model = User
        fields = ('username', 'password')

# ChangePasswordForm
class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(label=_('Old Password'), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'current-password', 'autofocus': True, 'class':'form-control'}))
    new_password1 = forms.CharField(label=_('New Password'), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'new password', 'class':'form-control'}),)
    new_password2 = forms.CharField(label=_('Confirm New Password'), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'new password', 'class':'form-control'}))


    class Meta:
        model = User
        fields = ('old_password', 'new_password1', 'new_password2')
        
# ResetPasswordForm
class ResetPasswordForm(PasswordResetForm):
    email = forms.EmailField(label=_('Email'), max_length=254, widget=forms.EmailInput(attrs={'autocomplete':'email', 'class':'form-control', 'placeholder':'Email'}))
    class Meta:
        model = User
        fields = ('email',)
        
# SetNewPasswordForm
class SetNewPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label=_('New Password'), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'new-password', 'class':'form-control'}))
    new_password2 = forms.CharField(label=_('Confirm New Password'), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'new-password', 'class':'form-control'}))

    class Meta:
        model = User
        fields = ('new_password1', 'new_password2')
        
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'division', 'district', 'thana', 'villorroad', 'phone', 'zipcode']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'division': forms.Select(attrs={'class': 'form-control'}),
            'district': forms.TextInput(attrs={'class': 'form-control'}),
            'thana': forms.TextInput(attrs={'class': 'form-control'}),
            'villorroad': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+880'}),
            'zipcode': forms.NumberInput(attrs={'class': 'form-control'}),
        }