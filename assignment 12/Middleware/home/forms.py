from django import forms
from home.models import Student

class Registration(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'roll': forms.NumberInput(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
            'passed_in_year': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'passed_out_year': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }