
from django import forms
from django.core.validators import RegexValidator
from home.models import Student, Department
"""
  | **Parameter**    | **Description**                                       | **Example**                                                                  |
| ---------------- | ----------------------------------------------------- | ---------------------------------------------------------------------------- |
| `label`          | Display name for the field                            | `name = forms.CharField(label='Full Name')`                                  |
| `label_suffix`   | Text shown after the label (like `:` or a space)      | `name = forms.CharField(label='Name', label_suffix=':')`                     |
| `initial`        | Default value for the field                           | `roll = forms.IntegerField(initial=101)`                                     |
| `required`       | Specifies whether input is mandatory (default = True) | `email = forms.EmailField(required=False)`                                   |
| `help_text`      | Small help message displayed below the field          | `age = forms.IntegerField(help_text='Enter your age in years')`              |
| `widget`         | Custom HTML input type or attributes                  | `dob = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))`      |
| `min_value`      | Minimum allowed numeric value                         | `age = forms.IntegerField(min_value=18)`                                     |
| `max_value`      | Maximum allowed numeric value                         | `age = forms.IntegerField(max_value=100)`                                    |
| `min_length`     | Minimum allowed text length                           | `username = forms.CharField(min_length=3)`                                   |
| `max_length`     | Maximum allowed text length                           | `username = forms.CharField(max_length=30)`                                  |
| `choices`        | Defines dropdown/select options                       | `gender = forms.ChoiceField(choices=[('M', 'Male'), ('F', 'Female')])`       |
| `disabled`       | Makes the field read-only (non-editable)              | `name = forms.CharField(initial='Faruk', disabled=True)`                     |
| `error_messages` | Custom error messages for validation errors           | `roll = forms.IntegerField(error_messages={'required': 'Roll is required'})` |
| `validators`     | Adds custom validation functions                      | `email = forms.EmailField(validators=[validate_email])`                      
| `auto_id`       | Automatically generates an `id` attribute for the field | `name = forms.CharField(auto_id='name_field')`                              |   
| `order          | 

  
"""

class RegistrationForm(forms.Form):

    # 1. label
    name = forms.CharField(
        label="Full Name"
    )

    # 2. label_suffix
    email = forms.EmailField(
        label="Email",
        label_suffix=":"
    )

    # 3. initial
    roll = forms.IntegerField(
        initial=101
    )

    # 4. required
    phone = forms.CharField(
        required=False
    )

    # 5. help_text
    age = forms.IntegerField(
        help_text="Enter your age"
    )

    # 6. widget
    dob = forms.DateField(
        widget=forms.DateInput(
            attrs={"type": "date"}
        )
    )

    # 7. min_value
    minimum_age = forms.IntegerField(
        min_value=18
    )

    # 8. max_value
    maximum_age = forms.IntegerField(
        max_value=100
    )

    # 9. min_length
    username = forms.CharField(
        min_length=3
    )

    # 10. max_length
    nickname = forms.CharField(
        max_length=30
    )

    # 11. choices
    gender = forms.ChoiceField(
        choices=[
            ("M", "Male"),
            ("F", "Female"),
            ("O", "Other"),
        ]
    )

    # 12. disabled
    readonly_name = forms.CharField(
        initial="Faruk",
        disabled=True
    )

    # 13. error_messages
    student_roll = forms.IntegerField(
        error_messages={
            "required": "Roll is required.",
            "invalid": "Enter a valid integer.",
            "min_value": "Roll must be positive.",
        },
        min_value=1
    )

    # 14. validators
    custom_email = forms.EmailField()

    # 15. auto_id
    # auto_id belongs to the Form constructor,
    # not the individual CharField.
    custom_name = forms.CharField()

    # 16. RegexValidator example
    code = forms.CharField(
        validators=[
            RegexValidator(
                regex=r"^[A-Z]{3}[0-9]{3}$",
                message="Enter a code like ABC123."
            )
        ]
    )

    # 17. ModelChoiceField
    department = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        empty_label="Select Department",
        required=True,
        label="Department"
    )

    # 18. FileField
    document = forms.FileField(
        required=False,
        label="Upload Document"
    )

    # 19. BooleanField
    agree = forms.BooleanField(
        required=True,
        label="I agree to the terms"
    )

    # 20. MultipleChoiceField
    skills = forms.MultipleChoiceField(
        choices=[
            ("python", "Python"),
            ("django", "Django"),
            ("sql", "SQL"),
        ],
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    # 21. EmailInput widget
    email_input = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"class": "form-control"}
        )
    )

    # 22. Textarea widget
    address = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "rows": 3,
                "placeholder": "Enter address"
            }
        )
    )

    # 23. PasswordInput widget
    password = forms.CharField(
        widget=forms.PasswordInput()
    )

    # 24. HiddenInput widget
    hidden_value = forms.CharField(
        initial="student",
        widget=forms.HiddenInput()
    )

    # 25. Field ordering
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["custom_name"].widget.attrs.update({
            "id": "custom_name",
            "class": "form-control",
        })

        self.order_fields([
            "name",
            "email",
            "roll",
            "age",
            "dob",
            "gender",
            "department",
            "skills",
            "document",
        ])
