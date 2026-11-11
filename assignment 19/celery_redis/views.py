from django.shortcuts import render
from django.views import View

from celery_redis.forms import EmailForm
from celery_redis.tasks import send_email_task


class HomeView(View):
    def get(self, request):
        form = EmailForm()
        return render(request, "celery_redis/home.html", {"form": form})

    def post(self, request):
        form = EmailForm(request.POST)
        if form.is_valid():
            send_email_task(form.cleaned_data["email"])
        return render(request, "celery_redis/home.html", {"form": form})
