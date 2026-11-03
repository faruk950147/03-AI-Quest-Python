from django.apps import AppConfig


class CeleryRedisConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'celery_redis'
