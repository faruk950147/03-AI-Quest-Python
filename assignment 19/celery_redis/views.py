from django.http import HttpResponse
from django.views import View
from celery_redis.tasks import (
    send_notification_email,
    add
)

class HomeView(View):
    def get(self, request):
        # send_notification_email("ferow74188@macsnipe.com")
        result = add.delay(4, 6)
        # result = add.apply_async([10, 20], countdown=10)
        print(
            f"Task ID: {result.id}, Status: {result.status} "
            f"Result: {result.get()} Ready: {result.ready()}"
        )
        return HttpResponse(
            f"Hello, this is the Home View! Task ID: {result.id}, "
            f"Status: {result.status}, Result: {result.get()}, "
            f"Ready: {result.ready()}"
        ) 
