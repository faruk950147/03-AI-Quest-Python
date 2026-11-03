from django.http import HttpResponse
from django.views import View
from celery_redis.tasks import (
    debug_task,
    send_welcome_email,
    send_welcome_email1,
)

class HomeView(View):
    def get(self, request):
        debug_task.delay()
        # send_welcome_email.delay("ferow74188@macsnipe.com")
        # send_welcome_email1("ferow74188@macsnipe.com")
        return HttpResponse("Hello, this is the Home View!") 
