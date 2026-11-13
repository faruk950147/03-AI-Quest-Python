from django.shortcuts import render
from django.http import JsonResponse
from django.views import View

import yfinance as yf

class HomeView(View):
    template_name = "app/home.html"
    def get(self, request):
        meta = yf.Ticker("META")
        print(meta.info)
        
        return render(request, 'app/home.html',)

