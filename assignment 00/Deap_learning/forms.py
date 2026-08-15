from django import forms

class StudentRegistrationForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
            
    name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'placeholder': 'Name'})
    )
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'placeholder': 'Username'})
    )
    phone = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'placeholder': 'Phone'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Email'})
    )
    department = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'placeholder': 'Department'})
    )
    session = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'placeholder': 'Session'})
    )
    password = forms.CharField(
        max_length=150,
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'})
    )
    password2 = forms.CharField(
        max_length=150,
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'})
    )