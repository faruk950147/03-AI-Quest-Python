from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from checkout.models import Shipping


# settings.AUTH_USER_MODEL
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_shipping(sender, instance, created, **kwargs):
    if created:
        Shipping.objects.create(user=instance)