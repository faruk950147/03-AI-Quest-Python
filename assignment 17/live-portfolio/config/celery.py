import os
from celery import Celery

# Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')

# Load CELERY_ settings from Django settings.py
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto discover tasks from all installed apps
app.autodiscover_tasks()

# Optional debug task (only for development)
@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request}')
