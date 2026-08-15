from django import forms
from task.models import Task

class TaskForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({'class': 'form-control', 'cols': '6', 'rows': '4'})
            else:
                field.widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Task
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'id': 'name'}),
            'department': forms.TextInput(attrs={'id': 'department'}),
            'phone': forms.TextInput(attrs={'id': 'phone'}),
            'is_completed': forms.CheckboxInput(attrs={'id': 'is_completed'})
        }