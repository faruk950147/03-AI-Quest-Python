from django.http import HttpResponse
from django.views import View
from celery_redis.tasks import (
    send_notification_email,
    add
)

class HomeView(View):
    def get(self, request):
        # send_notification_email("ferow74188@macsnipe.com", "This is a test notification.")
        result = add.delay(5, 3)
        print(f"Task ID: {result.id}, Status: {result.status} Result: {result.get()}")
        return HttpResponse(f"Hello, this is the Home View! Task ID: {result.id}, Status: {result.status}, Result: {result.get()}") 
