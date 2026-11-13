import logging

import yfinance as yf

from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

logger = logging.getLogger(__name__)


class HomeView(View):
    DEFAULT_SYMBOLS = [
        "BHARTIARTL.NS",
        "BAJFINANCE.NS",
        "BAJAJFINSV.NS",
        "RELIANCE.NS",
    ]

    def get_symbols(self, request):
        symbols_param = request.GET.get("symbols") or request.GET.get("symbol")

        if not symbols_param:
            return self.DEFAULT_SYMBOLS

        symbols = list(
            dict.fromkeys(
                s.strip().upper() for s in symbols_param.split(",") if s.strip()
            )
        )

        return symbols[:20]

    def fetch_stock(self, symbol, stock_id):
        try:
            ticker = yf.Ticker(symbol)
            df = ticker.history(period="5d")

            if df.empty:
                return None

            current = df.iloc[-1]

            current_price = float(current["Close"])

            previous_close = float(df["Close"].iloc[-2]) if len(df) > 1 else None

            change = current_price - previous_close if previous_close else 0

            change_pct = (change / previous_close) * 100 if previous_close else 0

            return {
                "id": stock_id,
                "symbol": symbol,
                "open": round(float(current["Open"]), 4),
                "high": round(float(current["High"]), 4),
                "low": round(float(current["Low"]), 4),
                "close": round(current_price, 4),
                "change": round(change, 4),
                "change_pct": round(change_pct, 2),
                "volume": int(current["Volume"]),  # <--- Volume ekhane add kora holo
            }

        except Exception:
            logger.exception("Error fetching stock: %s", symbol)
            return None

    def get(self, request):

        symbols = self.get_symbols(request)

        stock_list = []

        for symbol in symbols:
            stock = self.fetch_stock(symbol, len(stock_list) + 1)

            if stock:
                stock_list.append(stock)

        is_ajax = request.headers.get("x-requested-with") == "XMLHttpRequest"

        if is_ajax or "symbols" in request.GET:
            return JsonResponse({"stocks": stock_list})

        return render(request, "app/home.html", {"stocks": stock_list})
