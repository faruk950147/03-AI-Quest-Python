from django.shortcuts import render
from django.http import JsonResponse
from django.views import View

import yfinance as yf


class HomeView(View):
    def get(self, request):

        meta = yf.Ticker("META")

        data = meta.history(period="1y")

        data = data.to_html(classes="table table-striped table-bordered", border=0)

        context = {"data": data}

        return render(request, "app/home.html", context)