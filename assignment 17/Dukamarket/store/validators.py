from django.core.exceptions import ValidationError

def validate_image_size(image):
    max_size = 2 * 1024 * 1024  # 2MB
    if image.size > max_size:
        raise ValidationError("File size must be under 2MB!")
