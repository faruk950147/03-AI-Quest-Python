# tasks.py

from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def debug_task(self):
    print(f'Request: {self.request}')


@shared_task(
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_jitter=True,
    retry_kwargs={"max_retries": 3}
)
def send_welcome_email(email):
    send_mail(
        subject="Welcome!",
        message="Welcome to our platform.",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
        fail_silently=False,
    )
    return "Email sent successfully"


def send_welcome_email1(email):
    send_mail(
        subject="Welcome!",
        message="Welcome to our platform.",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
        fail_silently=False,
    )
    return "Email sent successfully"