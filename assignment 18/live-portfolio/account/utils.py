from django.core.mail import send_mail
from django.conf import settings
from django.utils.translation import gettext_lazy as _
import re

def send_email(subject, message, email):
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
        fail_silently=False,
    )

def normalize_phone_number(phone):
    if not phone:
        return None

    phone = str(phone)

    # remove spaces, dashes, brackets
    phone = re.sub(r"[\s\-()]", "", phone)

    # already correct format
    if phone.startswith("+880"):
        return phone

    # 880XXXXXXXXXX → +880XXXXXXXXXX
    if phone.startswith("880"):
        return "+" + phone

    # 01XXXXXXXXX → +8801XXXXXXXXX
    if phone.startswith("01") and len(phone) == 11:
        return "+880" + phone[1:]

    # already + but not valid format
    if phone.startswith("+"):
        return phone

    # invalid format fallback
    return None

