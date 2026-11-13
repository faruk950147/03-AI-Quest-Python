import re
import logging

import yfinance as yf

from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from django.core.cache import cache


class HomeView(View):
    template_name = "app/home.html"

    def get(self, request):

        symbol = request.GET.get("symbol", "AAPL").strip().upper()

        # Normal page request
        is_ajax = request.headers.get("X-Requested-With") == "XMLHttpRequest"

        if not is_ajax:
            return render(
                request, self.template_name, {"symbol": symbol if symbol else "AAPL"}
            )

        # Validate stock symbol
        if not re.fullmatch(r"[A-Z0-9.^=-]{1,20}", symbol):
            return JsonResponse({"error": "Invalid stock symbol."}, status=400)

        cache_key = f"stock_data_{symbol}"

        # Check cache
        cached_data = cache.get(cache_key)

        if cached_data is not None:
            return JsonResponse(cached_data)

        try:
            stock = yf.Ticker(symbol)

            # Intraday history
            history = stock.history(period="1d", interval="1m")

            if history.empty:
                return JsonResponse(
                    {"error": f"No stock data available for {symbol}."}, status=404
                )

            history_data = []

            for date, row in history.iterrows():
                history_data.append(
                    {
                        "date": date.strftime("%Y-%m-%d %H:%M:%S"),
                        "open": round(float(row["Open"]), 2),
                        "high": round(float(row["High"]), 2),
                        "low": round(float(row["Low"]), 2),
                        "close": round(float(row["Close"]), 2),
                        "volume": int(row["Volume"]),
                    }
                )

            latest = history_data[-1]

            # Previous trading day's closing price
            daily_history = stock.history(period="5d", interval="1d")

            previous_close = None

            if len(daily_history) >= 2:
                previous_close = float(daily_history["Close"].iloc[-2])

            elif len(daily_history) == 1:
                # Fallback: use the first intraday opening price
                previous_close = history_data[0]["open"]

            if previous_close and previous_close > 0:
                change = latest["close"] - previous_close
                change_percent = (change / previous_close) * 100
            else:
                change = 0
                change_percent = 0

            data = {
                "symbol": symbol,
                "history": history_data,
                "latest": latest,
                "previous_close": round(previous_close, 2)
                if previous_close is not None
                else None,
                "change": round(change, 2),
                "change_percent": round(change_percent, 2),
            }

            # Cache successful response for 30 seconds
            cache.set(cache_key, data, 30)

            return JsonResponse(data)

        except Exception:
            return JsonResponse(
                {"error": "Unable to fetch stock data. Please try again."}, status=502
            )
