from django.views.generic import View
from django.shortcuts import render

# Create your views here.
class ChatView(View):
    def get(self, request):
        return render(request, 'chat/chat.html')

