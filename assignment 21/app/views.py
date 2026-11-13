from django.shortcuts import render
from django.http import JsonResponse
from django.views import View

import yfinance as yf

import yfinance as yf

from django.shortcuts import render
from django.views import View


class HomeView(View):
    def get(self, request):

        meta = yf.Ticker("META")

        stock_data = meta.info

        context = {"stock": stock_data}

        return render(request, "app/home.html", context)

