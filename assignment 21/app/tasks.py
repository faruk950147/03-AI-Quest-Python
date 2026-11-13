from celery import shared_task


@shared_task
def additon(a, b):
    return a + b
