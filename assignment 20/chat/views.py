from django.shortcuts import render
from django.views import View

from chat.models import Messages


class HomeView(View):
    def get(self, request):
        messages = Messages.objects.select_related("user").order_by("-id")[:5]

        context = {
            "messages": messages,
        }

        return render(request, "chat/home.html", context)