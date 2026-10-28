
from django import forms
from django.core.validators import RegexValidator
from home.models import Department


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
