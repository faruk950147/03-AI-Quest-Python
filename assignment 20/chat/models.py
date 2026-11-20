from django.conf import settings
from django.db import models


class Messages(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="messages"
    )

    room_name = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "chat_messages"
        verbose_name_plural = "messages"
        ordering = ["id"]

    @classmethod
    def last_5_messages(cls, room_name):
        return (
            cls.objects.filter(room_name=room_name)
            .select_related("user")
            .order_by("id")[:5]
        )

    def __str__(self):
        return self.user.username
