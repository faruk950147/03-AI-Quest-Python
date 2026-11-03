from django.http import HttpResponse
from django.views import View
from celery_redis.tasks import debug_task

class HomeView(View):
    def get(self, request):
        debug_task.delay()  
        return HttpResponse("Hello, this is the Home View!") 
