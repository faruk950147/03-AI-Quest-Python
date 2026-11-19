from django.contrib import admin

from chat.models import Messages


@admin.register(Messages)
class MessagesAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "room_name", "content", "created_at", "updated_at")
    list_display_links = ("id", "user")
    list_filter = ("room_name", "created_at")
    search_fields = ("user__username", "room_name", "content")
    ordering = ("-id",)
    readonly_fields = ("created_at", "updated_at")
    list_per_page = 20
