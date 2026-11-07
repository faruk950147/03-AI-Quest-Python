from django  import forms

class EmailForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
        "class": "form-control", 
        "placeholder": "Enter your email address"}),
    )
    
    