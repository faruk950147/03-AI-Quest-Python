from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator, RegexValidator
from django.utils.translation import gettext_lazy as _

PHONE_REGEX = r"^\+?\d{10,15}$"
USERNAME_REGEX = r"^[a-zA-Z0-9_]+$"

phone_validator = RegexValidator(
    regex=PHONE_REGEX,
    message=_("Enter a valid phone number"),
)

username_validator = RegexValidator(
    regex=USERNAME_REGEX,
    message=_("Username can contain only letters, numbers and underscore"),
)

def validate_image_size(image):
    if not image:
        return

    if not image.storage.exists(image.name):
        return

    if image.size > 2 * 1024 * 1024:
        raise ValidationError("Image size must be under 2MB")

def validate_file_extension(value):
    valid_extensions = ['jpg', 'jpeg', 'png', 'gif']
    extension = value.name.split('.')[-1].lower()
    if extension not in valid_extensions:
        raise ValidationError(f"Unsupported file extension. Allowed extensions are: {', '.join(valid_extensions)}")
    