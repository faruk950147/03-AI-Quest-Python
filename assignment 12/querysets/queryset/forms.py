from django import forms
from queryset.models import Teacher, Student

class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.TextInput(attrs={'class': 'form-control'}),
            'salary': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        

class StudentForm(forms.ModelForm):

    class Meta:
        model = Student
        fields = '__all__'

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'roll': forms.NumberInput(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
            'passed_in_year': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'passed_out_year': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'marks': forms.NumberInput(attrs={'class': 'form-control'}),
        }