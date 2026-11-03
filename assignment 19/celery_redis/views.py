from django.http import HttpResponse
from django.views import View
from celery_redis.tasks import (
    debug_task, add_numbers, send_welcome_email, hello
)

class HomeView(View):
    def get(self, request):
        debug_task.delay()
        add_numbers.delay(5, 3)
        send_welcome_email.delay("kosiye9891@macsnipe.com")
        return HttpResponse("Hello, this is the Home View!") 
