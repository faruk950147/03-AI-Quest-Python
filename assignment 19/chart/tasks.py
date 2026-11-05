# tasks.py

from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task(
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_jitter=True,
    retry_kwargs={"max_retries": 3}
)
def send_notification_email(email):
    send_mail(
        subject="Notification",
        message="This is a notification email sent from Celery.",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
        fail_silently=False,
    )
    return "Notification email sent successfully"

@shared_task
def add(x, y):
    return x + y