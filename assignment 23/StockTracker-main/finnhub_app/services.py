
import os
import requests


def get_stock_data(symbol):
    """
    Retrieve stock quote data from Finnhub API.

    Returns:
        tuple: (stock_data, error_message)
    """

    if not symbol:
        return None, "Stock symbol is required."

    symbol = symbol.strip().upper()

    if not symbol.isalpha():
        return None, "Invalid stock symbol."

    api_key = os.getenv("FINNHUB_API_KEY")

    if not api_key:
        return None, "Finnhub API key is missing."

    url = "https://finnhub.io/api/v1/quote"

    params = {
        "symbol": symbol,
        "token": api_key
    }

    try:
        response = requests.get(
            url,
            params=params,
            timeout=10
        )

        if response.status_code == 401:
            return None, "Invalid Finnhub API key."

        if response.status_code == 403:
            return None, "Finnhub API access denied."

        if response.status_code == 429:
            return None, "Finnhub rate limit exceeded."

        response.raise_for_status()

        data = response.json()

        if not isinstance(data, dict):
            return None, "Invalid API response."

        price = data.get("c")

        if price is None or price <= 0:
            return None, f"No valid stock data found for {symbol}."

        return data, None

    except requests.exceptions.Timeout:
        return None, "Finnhub API request timed out."

    except requests.exceptions.HTTPError:
        return None, "Finnhub HTTP error."

    except requests.exceptions.RequestException:
        return None, "Network connection error."

    except (ValueError, TypeError):
        return None, "Invalid JSON response from Finnhub."
