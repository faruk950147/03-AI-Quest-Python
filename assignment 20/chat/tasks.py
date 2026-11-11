# tasks.py
from celery import shared_task

@shared_task
def additon(*args):
    print(f"Arguments received: {args}")

    return "Task executed successfully"