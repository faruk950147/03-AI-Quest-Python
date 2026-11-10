from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View

class ChatView(View):
    def get(self, request):
        return render(request, "chat/chat.html")
