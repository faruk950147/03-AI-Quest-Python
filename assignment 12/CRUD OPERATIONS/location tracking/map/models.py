from django.db import models

class PhoneSearch(models.Model):
    number = models.CharField(max_length=20, unique=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    provider = models.CharField(max_length=100, blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Phone Search Record"
        verbose_name_plural = "Phone Search Records"

    def __str__(self):
        return f"{self.number} ({self.location})"