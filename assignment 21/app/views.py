from django.shortcuts import render
from django.views import View

from yahoo_fin.stock_info import *


class HomeView(View):
    def get(self, request):
        # Fetch the Nifty 50 tickers list
        stock_picker = tickers_nifty50()
        
        # Print to console for debugging (optional)
        print(f'stock picker: {stock_picker}')
        
        # Pass the data to the template via context
        context = {
            'stock_picker': stock_picker
        }

        return render(request, "app/home.html", context)
