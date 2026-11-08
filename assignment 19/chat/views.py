from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from chat.forms import EmailForm
from chat.tasks import (
    send_notification_email,
    add
)
class HomeView(View):
    def get(self, request):
        return render(request, "chat/home.html")
    


class EmailSendView(View):
    def get(self, request):
        form = EmailForm()
        return render(request, "chat/send-email.html", {"form": form})
    def post(self, request):
        form = EmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            send_notification_email.delay(email)
            return redirect('send-email')
        return render(request, "chat/send-email.html", {"form": form})  

class chatView(View):
    def get(self, request):
        return render(request, "chat/chat.html")
