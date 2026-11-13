import logging

import yfinance as yf
from celery import shared_task

logger = logging.getLogger(__name__)


@shared_task
def real_data_updated(limit=12, days=8):
    symbols = [
        "BHARTIARTL.NS",
        "BAJFINANCE.NS",
        "BAJAJFINSV.NS",
        "RELIANCE.NS",
    ]

    results = []

    for symbol in symbols[:limit]:
        try:
            ticker = yf.Ticker(symbol)
            df = ticker.history(period=f"{days}d")

            if df.empty:
                continue

            current = df.iloc[-1]

            results.append(
                {
                    "symbol": symbol,
                    "open": round(float(current["Open"]), 2),
                    "high": round(float(current["High"]), 2),
                    "low": round(float(current["Low"]), 2),
                    "close": round(float(current["Close"]), 2),
                    "volume": int(current["Volume"]),
                }
            )

        except Exception:
            logger.exception("Stock update failed: %s", symbol)

    logger.info("Stock data updated: %s", results)

    return results
