# tasks.py
from celery import shared_task


@shared_task
def add(*args):
    return f"Notification sent to: {args}"