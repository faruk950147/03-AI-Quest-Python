# Realtime Stock Market – Complete Django Project Documentation
Correct WebSocket URLs
Purpose	URL
BTC/USDT trades	wss://stream.binance.com:9443/ws/btcusdt@trade
BTC/USDT ticker	wss://stream.binance.com:9443/ws/btcusdt@ticker
BTC/USDT order book	wss://stream.binance.com:9443/ws/btcusdt@depth
ETH/USDT trades	wss://stream.binance.com:9443/ws/ethusdt@trade

ws://127.0.0.1:8000/ws/chat/
## 1. Project Overview

**Project Name:** Realtime Stock Market  
**Project Type:** Advanced Python Django Backend Project  
**Backend:** Python, Django, Django REST Framework (DRF)  
**External API:** Finnhub Stock Market API  
**Realtime Communication:** Django Channels + WebSocket  
**Background Processing:** Celery + Celery Beat  
**Message Broker / Cache:** Redis  
**Database:** PostgreSQL (Production), SQLite (Development)  
**Frontend:** HTML, CSS, Bootstrap 5, JavaScript, Chart.js  
**Authentication:** Django Authentication + JWT  
**API Documentation:** drf-spectacular / Swagger UI  

### Project Description

Realtime Stock Market is a web-based application that allows users to monitor stock prices, track market movements, manage personal watchlists, manage investment portfolios, view historical stock data, and receive price alerts.

The application retrieves stock market data from the Finnhub API. Django REST Framework provides REST APIs, Django Channels handles WebSocket communication, and Celery performs background tasks such as fetching stock prices, updating historical data, and checking price alerts.

The application uses PostgreSQL for persistent data storage and Redis for background task processing and realtime communication.

### Main Goals

- Display current stock prices.
- Provide realtime price updates through WebSockets.
- Search for stocks using their symbols.
- Create and manage personal watchlists.
- Track stock investments through a portfolio.
- Display historical stock prices.
- Show stock market news.
- Create price alerts.
- Send notifications when stock prices reach target values.
- Provide secure REST APIs.
- Perform background tasks automatically.

---

# 2. Project Features

## 2.1 User Authentication

Users can:

- Register an account.
- Log in and log out.
- Obtain JWT access and refresh tokens.
- View their profile.
- Update their profile.
- Change their password.
- Access protected APIs.

**Authentication Technology:**

- Django Authentication System
- Django REST Framework
- Simple JWT

## 2.2 Stock Market Dashboard

The dashboard displays:

- Stock symbol.
- Company name.
- Current price.
- Previous closing price.
- Price change.
- Percentage change.
- Day's high and low.
- Trading volume.
- Last updated time.

Example:

| Symbol | Company | Price | Change |
|---|---|---:|---:|
| AAPL | Apple Inc. | $230.50 | +1.25% |
| MSFT | Microsoft | $420.30 | +0.85% |
| GOOGL | Alphabet | $175.20 | -0.45% |
| AMZN | Amazon | $195.80 | +2.10% |

*These values are illustrative, not live market data.*

## 2.3 Stock Search

Users can search stocks using:

- Stock symbol.
- Company name.
- Exchange.
- Stock category.

Example:

```text
AAPL
MSFT
GOOGL
AMZN
TSLA
NVDA
```

The backend retrieves stock information from the database or external market data provider.

## 2.4 Realtime Stock Price Updates

The application uses Django Channels and WebSockets to broadcast price updates to connected clients.

Features:

- Live price updates.
- Automatic dashboard updates.
- Multiple client connections.
- Stock-specific WebSocket groups.
- Connection and disconnection handling.

**Important:** Django Channels provides realtime communication between the backend and frontend. The backend still needs a data source, such as Finnhub WebSocket or a scheduled REST API polling task, to obtain market prices.

## 2.5 Watchlist Management

Users can:

- Add stocks to a watchlist.
- View watchlisted stocks.
- Remove stocks.
- View current prices.
- Track price movements.

Each user has their own watchlist.

## 2.6 Portfolio Management

Users can manage their investments.

Features:

- Add purchased stocks.
- Update holdings.
- Remove holdings.
- Track quantity.
- Store purchase price.
- Calculate current investment value.
- Calculate profit and loss.

Example:

| Symbol | Quantity | Average Buy Price | Current Price |
|---|---:|---:|---:|
| AAPL | 10 | $180 | $230 |
| MSFT | 5 | $350 | $420 |

### Portfolio Calculations

Current Value:

```python
current_value = quantity * current_price
```

Invested Amount:

```python
invested_amount = quantity * average_buy_price
```

Profit or Loss:

```python
profit_loss = current_value - invested_amount
```

Profit or Loss Percentage:

```python
profit_loss_percentage = (
    (profit_loss / invested_amount) * 100
    if invested_amount > 0
    else 0
)
```

For multiple purchases of the same stock, calculate the weighted average purchase price rather than simply averaging the transaction prices.

## 2.7 Historical Stock Data

Users can view historical stock prices.

Supported intervals may include:

- 1 minute.
- 5 minutes.
- 15 minutes.
- 30 minutes.
- 1 hour.
- 1 day.
- 1 week.

Historical data can be displayed using Chart.js.

Typical chart data:

- Open price.
- High price.
- Low price.
- Close price.
- Volume.

## 2.8 Stock Market News

Users can view:

- Latest market news.
- Company-specific news.
- News headlines.
- News summaries.
- Published dates.
- Source URLs.

News data can be retrieved from Finnhub or another supported news provider.

## 2.9 Price Alerts

Users can create price alerts.

Example:

```text
Stock: AAPL
Condition: Greater than
Target Price: 250
```

When the stock price reaches or exceeds the target, the system creates a notification.

Supported conditions:

- Greater than.
- Less than.
- Greater than or equal to.
- Less than or equal to.

Notification delivery can be implemented through:

- In-app notifications.
- Email.
- WebSocket events.

---

# 3. Technology Stack

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Django | Backend framework |
| Django REST Framework | REST API development |
| PostgreSQL | Production database |
| SQLite | Local development database |
| Finnhub API | External stock market data |
| Django Channels | WebSocket communication |
| Redis | Celery broker and Channels layer |
| Celery | Background task processing |
| Celery Beat | Scheduled tasks |
| Simple JWT | Token-based authentication |
| Bootstrap 5 | Frontend styling |
| JavaScript | Frontend interactions |
| Chart.js | Stock charts |
| Git & GitHub | Version control |
| Docker | Application containerization |
| Swagger / OpenAPI | API documentation |

---

# 4. System Architecture

```text
                    USER / BROWSER
                          |
             HTML + Bootstrap + JavaScript
                          |
             REST API / WebSocket Connection
                          |
              DJANGO APPLICATION SERVER
                          |
        +-----------------+-----------------+
        |                 |                 |
       DRF             Channels          Services
        |                 |                 |
   REST APIs          WebSocket       Business Logic
        |                 |                 |
        +-----------------+-----------------+
                          |
             +------------+------------+
             |                         |
        PostgreSQL                   Redis
             |                         |
       Persistent Data          Channels Layer
                                       |
                                  Celery Broker
                                       |
                              Celery Workers
                                       |
                                  Celery Beat
                                       |
                              Finnhub API
```

### Architecture Explanation

1. The frontend sends HTTP requests to Django REST APIs.
2. Django REST Framework validates requests and returns JSON responses.
3. Django services handle business logic.
4. PostgreSQL stores users, stocks, portfolios, watchlists, historical prices, and alerts.
5. Celery workers perform background operations.
6. Celery Beat schedules recurring tasks.
7. Redis acts as the Celery message broker and Channels communication layer.
8. Django Channels broadcasts stock updates to connected WebSocket clients.
9. Finnhub provides external stock market information.

**Important distinction:** Redis does not automatically fetch stock prices. Celery tasks or a Finnhub streaming client must retrieve market data before the application can broadcast it.

---

# 5. Project Folder Structure

Recommended structure:

```text
realtime-stock-market/
│
├── config/
│   ├── __init__.py
│   ├── asgi.py
│   ├── wsgi.py
│   ├── urls.py
│   ├── settings.py
│   └── celery.py
│
├── apps/
│   ├── accounts/
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── tests.py
│   │
│   ├── stocks/
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── services.py
│   │   ├── tasks.py
│   │   └── tests.py
│   │
│   ├── watchlists/
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── tests.py
│   │
│   ├── portfolios/
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── tests.py
│   │
│   ├── alerts/
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── tasks.py
│   │   └── tests.py
│   │
│   ├── notifications/
│   │   ├── models.py
│   │   ├── services.py
│   │   └── tasks.py
│   │
│   └── market_news/
│       ├── models.py
│       ├── serializers.py
│       ├── views.py
│       └── services.py
│
├── templates/
├── static/
├── media/
├── requirements.txt
├── .env
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
└── manage.py
```

### App Responsibilities

| App | Responsibility |
|---|---|
| accounts | Registration, login, profile, authentication |
| stocks | Stock information, quotes, historical prices |
| watchlists | User-specific stock watchlists |
| portfolios | Investment and holding management |
| alerts | Price alert rules and checking |
| notifications | Notification storage and delivery |
| market_news | Market news management |

---

# 6. Environment Setup

## 6.1 Create Project Directory

```bash
mkdir realtime-stock-market
cd realtime-stock-market
```

## 6.2 Create Virtual Environment

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

Linux / macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 6.3 Install Packages

```bash
pip install django
pip install djangorestframework
pip install djangorestframework-simplejwt
pip install django-cors-headers
pip install channels
pip install channels-redis
pip install celery
pip install redis
pip install django-environ
pip install psycopg[binary]
pip install requests
pip install drf-spectacular
pip install gunicorn
pip install uvicorn
```

Save dependencies:

```bash
pip freeze > requirements.txt
```

## 6.4 Create Django Project

```bash
django-admin startproject config .
```

Create apps:

```bash
python manage.py startapp accounts
python manage.py startapp stocks
python manage.py startapp watchlists
python manage.py startapp portfolios
python manage.py startapp alerts
python manage.py startapp notifications
python manage.py startapp market_news
```

Move the apps into the `apps/` directory and update their `AppConfig` paths.

## 6.5 Install and Run Redis

Redis must be available before running Celery or the Redis-backed Channels layer.

You can run Redis locally or through Docker:

```bash
docker run --name stock-redis -p 6379:6379 -d redis:7
```

Check Redis:

```bash
redis-cli ping
```

Expected response:

```text
PONG
```

---

# 7. Environment Variables

Create `.env`:

```env
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

DATABASE_URL=sqlite:///db.sqlite3

FINNHUB_API_KEY=your-finnhub-api-key

REDIS_URL=redis://127.0.0.1:6379/0

EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@example.com
EMAIL_HOST_PASSWORD=your-email-app-password
EMAIL_USE_TLS=True
```

For production, use PostgreSQL:

```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/stock_market_db
DEBUG=False
```

Never commit `.env` or real API keys to GitHub.

Create `.env.example` containing placeholder values only.

---

# 8. Django Settings Configuration

In `config/settings.py`:

```python
from pathlib import Path
import environ

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(
    DEBUG=(bool, False)
)

environ.Env.read_env(BASE_DIR / ".env")

SECRET_KEY = env("SECRET_KEY")
DEBUG = env.bool("DEBUG", default=False)

ALLOWED_HOSTS = env.list(
    "ALLOWED_HOSTS",
    default=["localhost", "127.0.0.1"]
)

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "rest_framework",
    "rest_framework_simplejwt",
    "corsheaders",
    "channels",
    "drf_spectacular",

    "apps.accounts",
    "apps.stocks",
    "apps.watchlists",
    "apps.portfolios",
    "apps.alerts",
    "apps.notifications",
    "apps.market_news",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

ASGI_APPLICATION = "config.asgi.application"

DATABASES = {
    "default": env.db(
        "DATABASE_URL",
        default="sqlite:///db.sqlite3"
    )
}

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_PAGINATION_CLASS": (
        "rest_framework.pagination.PageNumberPagination"
    ),
    "PAGE_SIZE": 20,
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": 15 * 60,
    "REFRESH_TOKEN_LIFETIME": 7 * 24 * 60 * 60,
}

CORS_ALLOWED_ORIGINS = [
    "http://127.0.0.1:8000",
    "http://localhost:8000",
]

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [env("REDIS_URL")],
        },
    },
}

CELERY_BROKER_URL = env(
    "REDIS_URL",
    default="redis://127.0.0.1:6379/0"
)

CELERY_RESULT_BACKEND = env(
    "REDIS_URL",
    default="redis://127.0.0.1:6379/0"
)

CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = "UTC"

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

LOGIN_URL = "/accounts/login/"
LOGOUT_REDIRECT_URL = "/accounts/login/"
```

For production, configure HTTPS, secure cookies, trusted origins, allowed hosts, database credentials, CORS, and secret management properly. Do not use permissive CORS settings without a specific reason.

---

# 9. Database Design

## 9.1 Stock Model

The Stock model stores company and stock-symbol information.

`apps/stocks/models.py`:

```python
from django.db import models


class Stock(models.Model):
    symbol = models.CharField(
        max_length=20,
        unique=True,
        db_index=True
    )

    company_name = models.CharField(max_length=255)

    exchange = models.CharField(
        max_length=100,
        blank=True
    )

    industry = models.CharField(
        max_length=150,
        blank=True
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["symbol"]

    def __str__(self):
        return self.symbol
```

## 9.2 Stock Price Model

Stores price snapshots.

```python
from django.db import models


class StockPrice(models.Model):
    stock = models.ForeignKey(
        "stocks.Stock",
        on_delete=models.CASCADE,
        related_name="price_snapshots"
    )

    current_price = models.DecimalField(
        max_digits=18,
        decimal_places=6
    )

    change = models.DecimalField(
        max_digits=18,
        decimal_places=6,
        null=True,
        blank=True
    )

    percent_change = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        null=True,
        blank=True
    )

    high_price = models.DecimalField(
        max_digits=18,
        decimal_places=6,
        null=True,
        blank=True
    )

    low_price = models.DecimalField(
        max_digits=18,
        decimal_places=6,
        null=True,
        blank=True
    )

    open_price = models.DecimalField(
        max_digits=18,
        decimal_places=6,
        null=True,
        blank=True
    )

    previous_close = models.DecimalField(
        max_digits=18,
        decimal_places=6,
        null=True,
        blank=True
    )

    volume = models.BigIntegerField(
        null=True,
        blank=True
    )

    provider_timestamp = models.DateTimeField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["stock", "-created_at"]),
        ]

    def __str__(self):
        return f"{self.stock.symbol} - {self.current_price}"
```

**Design note:** This model represents append-only price snapshots. Use `created_at` to record when the snapshot was stored. If you instead maintain one mutable latest-price record per stock, use a separate model with a unique stock relationship and `updated_at = models.DateTimeField(auto_now=True)`.

## 9.3 Watchlist Model

`apps/watchlists/models.py`:

```python
from django.conf import settings
from django.db import models


class Watchlist(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="watchlists"
    )

    stock = models.ForeignKey(
        "stocks.Stock",
        on_delete=models.CASCADE,
        related_name="watchlist_items"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "stock"],
                name="unique_user_stock_watchlist"
            )
        ]

    def __str__(self):
        return f"{self.user} - {self.stock.symbol}"
```

## 9.4 Portfolio Model

```python
from django.conf import settings
from django.db import models


class PortfolioHolding(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="portfolio_holdings"
    )

    stock = models.ForeignKey(
        "stocks.Stock",
        on_delete=models.CASCADE,
        related_name="portfolio_holdings"
    )

    quantity = models.DecimalField(
        max_digits=18,
        decimal_places=6
    )

    average_buy_price = models.DecimalField(
        max_digits=18,
        decimal_places=6
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "stock"],
                name="unique_user_stock_holding"
            )
        ]

    def __str__(self):
        return f"{self.user} - {self.stock.symbol}"
```

For a more accurate investment ledger, use a separate `PortfolioTransaction` model to record every buy and sell transaction. Calculate holdings and average buy price from the transaction history.

## 9.5 Historical Stock Candle Model

Historical market data should store OHLCV information.

```python
from django.db import models


class StockCandle(models.Model):
    INTERVAL_CHOICES = [
        ("1m", "1 Minute"),
        ("5m", "5 Minutes"),
        ("15m", "15 Minutes"),
        ("1h", "1 Hour"),
        ("1d", "1 Day"),
    ]

    stock = models.ForeignKey(
        "stocks.Stock",
        on_delete=models.CASCADE,
        related_name="candles"
    )

    interval = models.CharField(
        max_length=5,
        choices=INTERVAL_CHOICES
    )

    timestamp = models.DateTimeField()

    open_price = models.DecimalField(max_digits=18, decimal_places=6)
    high_price = models.DecimalField(max_digits=18, decimal_places=6)
    low_price = models.DecimalField(max_digits=18, decimal_places=6)
    close_price = models.DecimalField(max_digits=18, decimal_places=6)

    volume = models.BigIntegerField(default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["stock", "interval", "timestamp"],
                name="unique_stock_candle_interval_timestamp"
            )
        ]
        indexes = [
            models.Index(fields=["stock", "interval", "timestamp"]),
        ]
        ordering = ["timestamp"]
```

## 9.6 Price Alert Model

`apps/alerts/models.py`:

```python
from django.conf import settings
from django.db import models


class PriceAlert(models.Model):
    CONDITION_CHOICES = [
        ("above", "Above"),
        ("below", "Below"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="price_alerts"
    )

    stock = models.ForeignKey(
        "stocks.Stock",
        on_delete=models.CASCADE,
        related_name="price_alerts"
    )

    target_price = models.DecimalField(
        max_digits=18,
        decimal_places=6
    )

    condition = models.CharField(
        max_length=10,
        choices=CONDITION_CHOICES
    )

    is_active = models.BooleanField(default=True)
    triggered_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.stock.symbol} - {self.condition} {self.target_price}"
```

## 9.7 Notification Model

`apps/notifications/models.py`:

```python
from django.conf import settings
from django.db import models


class Notification(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications"
    )

    title = models.CharField(max_length=255)
    message = models.TextField()

    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
```

## 9.8 Market News Model

```python
from django.db import models


class MarketNews(models.Model):
    headline = models.CharField(max_length=500)

    summary = models.TextField(blank=True)

    source = models.CharField(max_length=150, blank=True)

    url = models.URLField(max_length=1000, unique=True)

    image_url = models.URLField(
        max_length=1000,
        blank=True
    )

    published_at = models.DateTimeField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-published_at"]

    def __str__(self):
        return self.headline
```

---

# 10. Database Migrations

After creating models:

```bash
python manage.py makemigrations
python manage.py migrate
```

Create admin user:

```bash
python manage.py createsuperuser
```

Register models in their respective `admin.py` files.

Example:

```python
from django.contrib import admin
from .models import Stock, StockPrice, StockCandle


admin.site.register(Stock)
admin.site.register(StockPrice)
admin.site.register(StockCandle)
```

---

# 11. Finnhub API Integration

## 11.1 What is Finnhub?

Finnhub is an external financial market data provider.

It provides APIs for:

- Stock quotes.
- Company profiles.
- Company news.
- Historical candles.
- Market information.
- Stock symbols.

Website:

https://finnhub.io/

Create an account and obtain an API key.

## 11.2 Configure API Key

Add the API key to `.env`:

```env
FINNHUB_API_KEY=your-api-key
```

## 11.3 Create Stock Service

`apps/stocks/services.py`:

```python
import requests

from django.conf import settings


class FinnhubService:
    BASE_URL = "https://finnhub.io/api/v1"

    def __init__(self):
        self.api_key = settings.FINNHUB_API_KEY

    def get_quote(self, symbol):
        url = f"{self.BASE_URL}/quote"

        response = requests.get(
            url,
            params={
                "symbol": symbol,
                "token": self.api_key,
            },
            timeout=10,
        )

        response.raise_for_status()

        data = response.json()

        if not data or data.get("c") is None:
            raise ValueError("No quote data available.")

        return data
```

Add the following setting:

```python
FINNHUB_API_KEY = env("FINNHUB_API_KEY")
```

## 11.4 Understanding Quote Response

A typical Finnhub quote response contains:

```json
{
    "c": 230.50,
    "d": 2.85,
    "dp": 1.25,
    "h": 232.00,
    "l": 226.50,
    "o": 227.00,
    "pc": 227.65,
    "t": 1731931200
}
```

| Field | Meaning |
|---|---|
| c | Current price |
| d | Change |
| dp | Percentage change |
| h | Day high |
| l | Day low |
| o | Open price |
| pc | Previous close |
| t | Provider timestamp |

The exact fields and availability depend on the API endpoint and provider response.

---

# 12. Save Stock Prices to the Database

Create a shared service to retrieve and persist quotes.

`apps/stocks/services.py`:

```python
from datetime import datetime, timezone as datetime_timezone

from django.utils import timezone

from apps.stocks.models import Stock, StockPrice


def save_stock_quote(symbol):
    stock = Stock.objects.get(
        symbol=symbol.upper(),
        is_active=True
    )

    service = FinnhubService()
    quote = service.get_quote(stock.symbol)

    provider_timestamp = None

    if quote.get("t"):
        provider_timestamp = datetime.fromtimestamp(
            quote["t"],
            tz=datetime_timezone.utc
        )

    price = StockPrice.objects.create(
        stock=stock,
        current_price=quote["c"],
        change=quote.get("d"),
        percent_change=quote.get("dp"),
        high_price=quote.get("h"),
        low_price=quote.get("l"),
        open_price=quote.get("o"),
        previous_close=quote.get("pc"),
        provider_timestamp=provider_timestamp,
    )

    return price
```

This function is reusable by:

- API views.
- Celery tasks.
- Management commands.
- Scheduled background jobs.

Use this shared service rather than implementing different price-saving logic in multiple places.

---

# 13. Django REST Framework APIs

## 13.1 Stock Serializer

`apps/stocks/serializers.py`:

```python
from rest_framework import serializers

from .models import Stock, StockPrice


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = "__all__"


class StockPriceSerializer(serializers.ModelSerializer):
    symbol = serializers.CharField(
        source="stock.symbol",
        read_only=True
    )

    class Meta:
        model = StockPrice
        fields = [
            "id",
            "symbol",
            "current_price",
            "change",
            "percent_change",
            "high_price",
            "low_price",
            "open_price",
            "previous_close",
            "volume",
            "provider_timestamp",
            "created_at",
        ]
```

## 13.2 Stock List API

`apps/stocks/views.py`:

```python
from rest_framework import generics
from rest_framework.permissions import AllowAny

from .models import Stock
from .serializers import StockSerializer


class StockListAPIView(generics.ListAPIView):
    queryset = Stock.objects.filter(is_active=True)
    serializer_class = StockSerializer
    permission_classes = [AllowAny]
    search_fields = ["symbol", "company_name"]
```

## 13.3 Latest Stock Price API

```python
from rest_framework import generics
from rest_framework.permissions import AllowAny

from .models import StockPrice
from .serializers import StockPriceSerializer


class LatestStockPriceAPIView(generics.ListAPIView):
    serializer_class = StockPriceSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        symbol = self.kwargs["symbol"].upper()

        return (
            StockPrice.objects
            .filter(stock__symbol=symbol)
            .order_by("-created_at")[:1]
        )
```

## 13.4 Manual Stock Refresh API

```python
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .services import save_stock_quote
from .serializers import StockPriceSerializer


class RefreshStockAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, symbol):
        try:
            price = save_stock_quote(symbol)

            return Response(
                StockPriceSerializer(price).data,
                status=status.HTTP_200_OK
            )

        except Exception as exc:
            return Response(
                {"detail": str(exc)},
                status=status.HTTP_400_BAD_REQUEST
            )
```

For production, catch specific exceptions rather than exposing arbitrary exception messages to clients. Validate symbols and handle provider errors separately.

## 13.5 Stock URL Configuration

`apps/stocks/urls.py`:

```python
from django.urls import path

from .views import (
    StockListAPIView,
    LatestStockPriceAPIView,
    RefreshStockAPIView,
)

urlpatterns = [
    path("", StockListAPIView.as_view(), name="stock-list"),
    path(
        "<str:symbol>/latest/",
        LatestStockPriceAPIView.as_view(),
        name="stock-latest"
    ),
    path(
        "<str:symbol>/refresh/",
        RefreshStockAPIView.as_view(),
        name="stock-refresh"
    ),
]
```

---

# 14. Authentication APIs

Install:

```bash
pip install djangorestframework-simplejwt
```

Configure authentication in `settings.py` as described earlier.

`config/urls.py`:

```python
from django.contrib import admin
from django.urls import include, path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("admin/", admin.site.urls),

    path(
        "api/auth/token/",
        TokenObtainPairView.as_view(),
        name="token_obtain_pair"
    ),

    path(
        "api/auth/token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh"
    ),

    path("api/stocks/", include("apps.stocks.urls")),
]
```

### JWT Login Request

```http
POST /api/auth/token/
Content-Type: application/json
```

Request:

```json
{
    "username": "faruk",
    "password": "your-password"
}
```

Example response:

```json
{
    "refresh": "refresh-token",
    "access": "access-token"
}
```

Send the access token in protected requests:

```http
Authorization: Bearer ACCESS_TOKEN
```

Registration, profile, password change, and account management endpoints should be implemented in the accounts app.

---

# 15. Celery Background Processing

## 15.1 What is Celery?

Celery is a distributed task queue used to execute background operations.

Examples:

- Fetching stock prices.
- Updating historical market data.
- Checking price alerts.
- Sending notification emails.
- Processing market news.

## 15.2 Create Celery Configuration

`config/celery.py`:

```python
import os

from celery import Celery

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "config.settings"
)

app = Celery("config")

app.config_from_object(
    "django.conf:settings",
    namespace="CELERY"
)

app.autodiscover_tasks()
```

Update `config/__init__.py`:

```python
from .celery import app as celery_app

__all__ = ("celery_app",)
```

## 15.3 Create Stock Update Task

`apps/stocks/tasks.py`:

```python
from celery import shared_task

from .models import Stock
from .services import save_stock_quote


@shared_task(
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 3},
)
def update_stock_price(symbol):
    return save_stock_quote(symbol).id


@shared_task
def update_all_stock_prices():
    symbols = Stock.objects.filter(
        is_active=True
    ).values_list("symbol", flat=True)

    results = []

    for symbol in symbols:
        try:
            price = save_stock_quote(symbol)
            results.append({
                "symbol": symbol,
                "price_id": price.id,
                "status": "success",
            })

        except Exception as exc:
            results.append({
                "symbol": symbol,
                "status": "failed",
                "error": str(exc),
            })

    return results
```

For larger applications, avoid making too many simultaneous provider requests. Consider individual queued tasks, rate limits, bounded concurrency, and provider-specific retry policies.

## 15.4 Celery Beat Configuration

In `config/settings.py`:

```python
from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    "update-stock-prices-every-five-minutes": {
        "task": "apps.stocks.tasks.update_all_stock_prices",
        "schedule": 300.0,
    },
}
```

The schedule above is an example. Choose an interval that complies with the Finnhub plan, endpoint limits, market hours, and application requirements.

## 15.5 Run Celery Worker

```bash
celery -A config worker -l info
```

Windows development:

```bash
celery -A config worker -l info --pool=solo
```

## 15.6 Run Celery Beat

In another terminal:

```bash
celery -A config beat -l info
```

Celery Beat schedules tasks; Celery workers execute them. Run both processes when using scheduled background tasks.

---

# 16. Django Channels and WebSockets

## 16.1 What is Django Channels?

Django Channels extends Django to support asynchronous protocols such as WebSockets.

WebSockets allow a persistent, two-way communication channel between the browser and backend.

Unlike repeated HTTP polling, the server can send updates to clients whenever new data is available.

## 16.2 Configure ASGI

`config/asgi.py`:

```python
import os

from django.core.asgi import get_asgi_application

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "config.settings"
)

django_asgi_app = get_asgi_application()

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator

from apps.stocks.routing import websocket_urlpatterns


application = ProtocolTypeRouter({
    "http": django_asgi_app,

    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(websocket_urlpatterns)
        )
    ),
})
```

For production, use an authentication mechanism appropriate for the WebSocket client, enforce permissions for subscribed stock symbols, and validate allowed origins.

## 16.3 Create Stock Consumer

`apps/stocks/consumers.py`:

```python
import json

from channels.generic.websocket import AsyncWebsocketConsumer


class StockConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.symbol = self.scope["url_route"]["kwargs"][
            "symbol"
        ].upper()

        self.group_name = f"stock_{self.symbol}"

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def stock_update(self, event):
        await self.send(
            text_data=json.dumps(event["data"])
        )
```

## 16.4 WebSocket Routing

`apps/stocks/routing.py`:

```python
from django.urls import re_path

from .consumers import StockConsumer


websocket_urlpatterns = [
    re_path(
        r"ws/stocks/(?P<symbol>[A-Za-z0-9._-]+)/$",
        StockConsumer.as_asgi()
    ),
]
```

## 16.5 Broadcast Stock Price Updates

Create a helper:

`apps/stocks/websocket.py`:

```python
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


def broadcast_stock_update(symbol, data):
    channel_layer = get_channel_layer()

    async_to_sync(channel_layer.group_send)(
        f"stock_{symbol.upper()}",
        {
            "type": "stock.update",
            "data": data,
        }
    )
```

Call this function after successfully saving a new stock price.

For example:

```python
from apps.stocks.websocket import broadcast_stock_update


broadcast_stock_update(
    stock.symbol,
    {
        "symbol": stock.symbol,
        "current_price": str(price.current_price),
        "created_at": price.created_at.isoformat(),
    }
)
```

For a production system, move the broadcast operation to an appropriate background workflow if it should not block the request or price ingestion process.

## 16.6 Frontend WebSocket Example

```javascript
const symbol = "AAPL";

const socket = new WebSocket(
    `ws://127.0.0.1:8000/ws/stocks/${symbol}/`
);

socket.onopen = function () {
    console.log("WebSocket connected");
};

socket.onmessage = function (event) {
    const data = JSON.parse(event.data);

    console.log("Stock update:", data);

    document.getElementById("stock-price").textContent =
        data.current_price;
};

socket.onclose = function () {
    console.log("WebSocket disconnected");
};

socket.onerror = function (error) {
    console.error("WebSocket error:", error);
};
```

Use `wss://` instead of `ws://` when the production site uses HTTPS.

---

# 17. Historical Stock Data API

Historical candle data can be retrieved from Finnhub's stock candle endpoint.

Example request:

```text
GET https://finnhub.io/api/v1/stock/candle
```

Typical parameters:

```text
symbol=AAPL
resolution=D
from=START_UNIX_TIMESTAMP
to=END_UNIX_TIMESTAMP
token=YOUR_API_KEY
```

Example service:

```python
import requests

from django.conf import settings


def get_historical_candles(symbol, resolution, start_time, end_time):
    response = requests.get(
        "https://finnhub.io/api/v1/stock/candle",
        params={
            "symbol": symbol,
            "resolution": resolution,
            "from": start_time,
            "to": end_time,
            "token": settings.FINNHUB_API_KEY,
        },
        timeout=15,
    )

    response.raise_for_status()

    return response.json()
```

The response commonly contains arrays for:

- `o`: Open.
- `h`: High.
- `l`: Low.
- `c`: Close.
- `v`: Volume.
- `t`: Timestamp.
- `s`: Response status.

Validate the response status and array lengths before storing candles.

Use database uniqueness constraints and `update_or_create()` or bulk upserts to avoid duplicate candle records.

---

# 18. Price Alert System

## 18.1 Alert Checking Logic

Example:

```python
def is_alert_triggered(alert, current_price):
    if alert.condition == "above":
        return current_price >= alert.target_price

    if alert.condition == "below":
        return current_price <= alert.target_price

    return False
```

## 18.2 Check Alerts

A background task should:

1. Retrieve active alerts.
2. Get the latest price for each stock.
3. Compare the price with the alert target.
4. Mark matching alerts as triggered.
5. Create a notification.
6. Send an email if the user enabled email notifications.
7. Broadcast an event if the user is connected.

Use database transactions or conditional updates to prevent the same alert from triggering multiple times when multiple workers process it concurrently.

For production, also consider alert re-arming, notification delivery failures, and duplicate event prevention.

---

# 19. Notification System

Notification types:

- Price alert notification.
- Portfolio update notification.
- Market news notification.
- System notification.

Example notification:

```json
{
    "title": "Stock Price Alert",
    "message": "AAPL reached your target price.",
    "is_read": false
}
```

Recommended APIs:

```text
GET    /api/notifications/
GET    /api/notifications/unread/
PATCH  /api/notifications/{id}/read/
DELETE /api/notifications/{id}/
```

Every notification endpoint must restrict access to the authenticated user's own notifications.

---

# 20. Market News Integration

Retrieve news from the provider using its company-news or general-news endpoints.

Recommended workflow:

1. Request news from the provider.
2. Validate the response.
3. Normalize the news data.
4. Save records using a unique URL or provider ID.
5. Return paginated news through DRF.
6. Refresh news periodically using Celery Beat.

Example API:

```text
GET /api/news/
GET /api/news/company/AAPL/
```

Do not assume that all news endpoints are available on every provider plan.

---

# 21. Recommended API Endpoints

Base URL:

```text
/api/
```

## Authentication

| Method | Endpoint | Description |
|---|---|---|
| POST | `/auth/register/` | Register user |
| POST | `/auth/token/` | Login and obtain JWT |
| POST | `/auth/token/refresh/` | Refresh JWT |
| GET | `/auth/profile/` | View profile |
| PATCH | `/auth/profile/` | Update profile |
| POST | `/auth/logout/` | Logout / token blacklist, if enabled |

## Stocks

| Method | Endpoint | Description |
|---|---|---|
| GET | `/stocks/` | List stocks |
| GET | `/stocks/{symbol}/` | Stock details |
| GET | `/stocks/{symbol}/latest/` | Latest stored price |
| POST | `/stocks/{symbol}/refresh/` | Request manual refresh |
| GET | `/stocks/{symbol}/history/` | Historical price data |
| GET | `/stocks/search/?q=AAPL` | Search stocks |

## Watchlists

| Method | Endpoint | Description |
|---|---|---|
| GET | `/watchlists/` | View watchlist |
| POST | `/watchlists/` | Add stock |
| DELETE | `/watchlists/{id}/` | Remove stock |

## Portfolio

| Method | Endpoint | Description |
|---|---|---|
| GET | `/portfolio/` | View holdings |
| POST | `/portfolio/` | Add holding |
| GET | `/portfolio/{id}/` | Holding details |
| PATCH | `/portfolio/{id}/` | Update holding |
| DELETE | `/portfolio/{id}/` | Remove holding |
| GET | `/portfolio/summary/` | Portfolio summary |

## Alerts

| Method | Endpoint | Description |
|---|---|---|
| GET | `/alerts/` | List alerts |
| POST | `/alerts/` | Create alert |
| PATCH | `/alerts/{id}/` | Update alert |
| DELETE | `/alerts/{id}/` | Delete alert |

## Notifications

| Method | Endpoint | Description |
|---|---|---|
| GET | `/notifications/` | List notifications |
| GET | `/notifications/unread/` | Unread notifications |
| PATCH | `/notifications/{id}/read/` | Mark as read |

## News

| Method | Endpoint | Description |
|---|---|---|
| GET | `/news/` | Latest market news |
| GET | `/news/company/{symbol}/` | Company news |

## WebSocket

```text
ws://localhost:8000/ws/stocks/AAPL/
```

---

# 22. API Documentation with Swagger

Install:

```bash
pip install drf-spectacular
```

Configure the schema settings:

```python
REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}
```

Add URLs:

```python
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)

urlpatterns += [
    path(
        "api/schema/",
        SpectacularAPIView.as_view(),
        name="schema"
    ),

    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(
            url_name="schema"
        ),
        name="swagger-ui"
    ),
]
```

Open:

```text
http://127.0.0.1:8000/api/docs/
```

---

# 23. Frontend Development

Recommended frontend pages:

```text
Home / Dashboard
Login
Registration
Stock List
Stock Details
Watchlist
Portfolio
Price Alerts
Notifications
Market News
User Profile
```

## Dashboard Components

- Market overview.
- Stock price cards.
- Top gainers.
- Top losers.
- Watchlist summary.
- Portfolio summary.
- Stock price chart.
- Latest market news.

## Chart.js Example

```html
<canvas id="stockChart"></canvas>

<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

<script>
const context = document
    .getElementById("stockChart")
    .getContext("2d");

const stockChart = new Chart(context, {
    type: "line",

    data: {
        labels: ["09:00", "10:00", "11:00", "12:00", "13:00"],

        datasets: [{
            label: "AAPL Price",

            data: [220, 222, 221, 225, 230],

            borderWidth: 2,
            tension: 0.3
        }]
    },

    options: {
        responsive: true,
        maintainAspectRatio: false
    }
});
</script>
```

The example uses sample data. In the actual application, load chart data from the historical stock API.

---

# 24. Error Handling

The application should handle errors from:

- Invalid stock symbols.
- Invalid API requests.
- Expired JWT tokens.
- External API failures.
- Finnhub rate limits.
- Redis connection failures.
- Database errors.
- WebSocket disconnections.
- Invalid portfolio values.
- Duplicate watchlist entries.
- Missing historical data.

Recommended HTTP status codes:

| Status | Meaning |
|---|---|
| 200 | Successful request |
| 201 | Resource created |
| 204 | Successful deletion |
| 400 | Invalid request |
| 401 | Authentication required |
| 403 | Permission denied |
| 404 | Resource not found |
| 429 | Rate limit exceeded |
| 500 | Internal server error |
| 503 | External service unavailable |

Never expose API keys, passwords, stack traces, or internal database details in public API responses.

---

# 25. Security Best Practices

## Authentication

- Use JWT or secure session authentication.
- Set reasonable access-token expiration.
- Use refresh-token rotation and blacklisting where appropriate.
- Protect private endpoints.
- Never store plaintext passwords.

## Authorization

- Users can only access their own portfolios.
- Users can only access their own watchlists.
- Users can only manage their own alerts.
- Users can only access their own notifications.
- Validate WebSocket subscriptions and permissions.

## API Security

- Validate request data.
- Use DRF permissions.
- Add rate limiting.
- Restrict CORS origins.
- Use HTTPS in production.
- Protect against SQL injection through Django ORM.
- Keep Django and dependencies updated.

## Environment Security

- Keep secret keys in environment variables.
- Never upload `.env` to GitHub.
- Protect Finnhub API keys.
- Use secure database credentials.
- Disable `DEBUG` in production.

---

# 26. Testing

Testing is essential before deployment.

Recommended test categories:

## Unit Tests

- Stock model tests.
- Portfolio calculation tests.
- Price alert condition tests.
- Service validation tests.

## API Tests

- Registration.
- Login.
- JWT authentication.
- Stock listing.
- Stock search.
- Watchlist CRUD.
- Portfolio CRUD.
- Alert CRUD.
- Notification permissions.

## Integration Tests

- Finnhub API integration.
- Celery task execution.
- Redis communication.
- WebSocket message delivery.
- Database persistence.

## Example Model Test

```python
from django.test import TestCase

from apps.stocks.models import Stock


class StockModelTest(TestCase):

    def test_create_stock(self):
        stock = Stock.objects.create(
            symbol="AAPL",
            company_name="Apple Inc."
        )

        self.assertEqual(stock.symbol, "AAPL")
        self.assertEqual(stock.company_name, "Apple Inc.")
```

## Example Portfolio Calculation Test

```python
from decimal import Decimal

from django.test import SimpleTestCase


class PortfolioCalculationTest(SimpleTestCase):

    def test_profit_loss(self):
        quantity = Decimal("10")
        buy_price = Decimal("100")
        current_price = Decimal("120")

        invested = quantity * buy_price
        current_value = quantity * current_price

        profit_loss = current_value - invested

        self.assertEqual(profit_loss, Decimal("200"))
```

Run tests:

```bash
python manage.py test
```

Mock external Finnhub requests during automated tests so that tests do not depend on live market data or API availability.

---

# 27. Docker Configuration

Docker helps run the application and its supporting services consistently.

## Dockerfile

```dockerfile
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "config.asgi:application", "--host", "0.0.0.0", "--port", "8000"]
```

## docker-compose.yml

```yaml
services:
  web:
    build: .
    command: uvicorn config.asgi:application --host 0.0.0.0 --port 8000
    ports:
      - "8000:8000"
    env_file:
      - .env
    depends_on:
      - db
      - redis

  db:
    image: postgres:16
    environment:
      POSTGRES_DB: stock_market_db
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7
    ports:
      - "6379:6379"

  celery:
    build: .
    command: celery -A config worker -l info
    env_file:
      - .env
    depends_on:
      - db
      - redis

  celery-beat:
    build: .
    command: celery -A config beat -l info
    env_file:
      - .env
    depends_on:
      - db
      - redis

volumes:
  postgres_data:
```

The Docker Compose example is a development starting point. Configure a PostgreSQL `DATABASE_URL` that points to the `db` service, add health checks, and configure production secrets and persistence before deployment. Run only one Celery Beat scheduler for a given schedule.

Start services:

```bash
docker compose up --build
```

Run migrations:

```bash
docker compose exec web python manage.py migrate
```

---

# 28. Deployment

Possible deployment platforms:

- VPS.
- AWS.
- DigitalOcean.
- Render.
- Railway.
- Other ASGI-compatible hosting platforms.

Production deployment requirements:

1. Configure PostgreSQL.
2. Configure Redis.
3. Configure environment variables.
4. Set `DEBUG=False`.
5. Configure `ALLOWED_HOSTS`.
6. Configure HTTPS.
7. Configure static and media files.
8. Run database migrations.
9. Start the ASGI server.
10. Start Celery workers.
11. Start Celery Beat.
12. Configure logging and monitoring.
13. Configure backups.
14. Monitor API usage and provider limits.

For WebSocket support, ensure the reverse proxy and hosting platform support WebSocket upgrades.

---

# 29. Performance Optimization

Recommended improvements:

- Add database indexes.
- Use `select_related()` for foreign-key relationships.
- Use `prefetch_related()` for reverse and many-to-many relationships.
- Paginate API responses.
- Cache frequently requested stock data.
- Avoid unnecessary Finnhub API requests.
- Use background tasks for slow operations.
- Use bulk database operations when appropriate.
- Keep WebSocket messages small.
- Limit historical chart data by date range and interval.
- Monitor database query performance.

Example:

```python
stocks = StockPrice.objects.select_related(
    "stock"
).order_by("-created_at")
```

Redis caching can reduce repeated requests for frequently accessed stock information. Cache expiration should account for market hours and the freshness requirements of the data.

---

# 30. Finnhub API Rate Limits and Reliability

External API limits depend on the provider's current plan and endpoint.

The application should:

- Check the current Finnhub plan limits.
- Handle HTTP 429 responses.
- Use exponential backoff.
- Add request timeouts.
- Avoid duplicate requests.
- Cache suitable responses.
- Log provider errors.
- Avoid unnecessary polling.
- Handle market holidays and closed-market periods.

A successful HTTP response does not always mean valid stock data was returned. Validate the response content before saving it.

For realtime market data, evaluate whether Finnhub's WebSocket service is available under the chosen plan. If using Finnhub WebSocket directly, manage its connection, subscription messages, reconnect behavior, and provider limits separately from Django Channels.

---

# 31. Development Roadmap

Build the project step by step.

## Phase 1 – Project Setup

- Create Django project.
- Create virtual environment.
- Install dependencies.
- Configure environment variables.
- Configure PostgreSQL.
- Create Django apps.

## Phase 2 – Authentication

- User registration.
- JWT login.
- Token refresh.
- User profile.
- Permissions.

## Phase 3 – Stock Management

- Create Stock model.
- Create StockPrice model.
- Add stock records.
- Integrate Finnhub API.
- Save stock quotes.
- Build stock APIs.

## Phase 4 – Watchlist

- Create Watchlist model.
- Add stock to watchlist.
- Remove stock.
- List user watchlist.
- Handle duplicate entries.

## Phase 5 – Portfolio

- Create portfolio models.
- Add holdings.
- Update holdings.
- Remove holdings.
- Calculate investment value.
- Calculate profit and loss.

## Phase 6 – Background Processing

- Configure Redis.
- Configure Celery.
- Create background tasks.
- Configure Celery Beat.
- Fetch stock prices automatically.

## Phase 7 – WebSockets

- Install Django Channels.
- Configure ASGI.
- Create WebSocket consumer.
- Create WebSocket routing.
- Broadcast stock updates.
- Connect frontend.

## Phase 8 – Historical Data

- Create StockCandle model.
- Retrieve historical candles.
- Store historical data.
- Create history APIs.
- Build Chart.js charts.

## Phase 9 – Price Alerts

- Create alert model.
- Create alert APIs.
- Check alert conditions.
- Create notifications.
- Send email notifications.

## Phase 10 – Market News

- Integrate market news provider.
- Store news.
- Create news APIs.
- Build news dashboard.

## Phase 11 – Testing and Optimization

- Write unit tests.
- Write API tests.
- Test WebSockets.
- Test Celery.
- Optimize database queries.
- Add caching.
- Add pagination.

## Phase 12 – Deployment

- Configure Docker.
- Configure production database.
- Configure Redis.
- Deploy Django ASGI application.
- Deploy Celery workers.
- Configure HTTPS.
- Add logging and monitoring.

---

# 32. Git and GitHub

Initialize Git:

```bash
git init
```

Create `.gitignore`:

```gitignore
.venv/
venv/
__pycache__/
*.pyc

.env
db.sqlite3

staticfiles/
media/

.idea/
.vscode/

.coverage
htmlcov/
```

Add files:

```bash
git add .
git commit -m "Initial project setup"
```

Create GitHub repository and connect:

```bash
git remote add origin YOUR_GITHUB_REPOSITORY_URL
git branch -M main
git push -u origin main
```

Never commit real API keys, passwords, or production database credentials.

---

# 33. Interview Questions and Answers

## Q1. What is Django?

Django is a high-level Python web framework used to build secure and maintainable web applications quickly. It provides ORM, authentication, URL routing, middleware, admin panel, and many built-in features.

## Q2. What is Django REST Framework?

Django REST Framework is a toolkit for building RESTful APIs using Django. It provides serializers, API views, authentication, permissions, pagination, and browsable API support.

## Q3. What is Finnhub?

Finnhub is a financial data provider that offers stock market information through REST APIs and WebSocket services, depending on the available plan.

## Q4. What is Celery?

Celery is a distributed task queue that executes background tasks outside the normal HTTP request-response cycle.

## Q5. Why use Celery?

Celery is useful for slow or scheduled operations such as stock price fetching, alert checking, email sending, and news updates.

## Q6. What is Redis?

Redis is an in-memory data store. In this project, Redis can act as the Celery message broker, task result backend, and Django Channels communication layer.

## Q7. What is Celery Beat?

Celery Beat is a scheduler that periodically sends tasks to Celery workers.

## Q8. What is Django Channels?

Django Channels extends Django to support asynchronous protocols, including WebSockets.

## Q9. What is a WebSocket?

A WebSocket is a persistent, bidirectional communication protocol that allows the client and server to exchange messages without repeatedly opening new HTTP requests.

## Q10. What is the difference between HTTP and WebSocket?

HTTP usually follows a request-response pattern. WebSocket maintains a persistent connection and allows both the client and server to send messages.

## Q11. What is JWT?

JWT stands for JSON Web Token. It is a token-based authentication mechanism used to authenticate API requests.

## Q12. What is Django ORM?

Django ORM allows developers to interact with databases using Python objects instead of writing raw SQL for every operation.

## Q13. What is PostgreSQL?

PostgreSQL is an open-source relational database management system known for reliability, data integrity, and advanced SQL features.

## Q14. Why use PostgreSQL instead of SQLite in production?

PostgreSQL is generally more suitable for production workloads involving concurrent users, complex queries, transactions, and larger datasets. SQLite is useful for lightweight development and testing.

## Q15. What is an API?

An API is an interface that allows different software applications to communicate with each other.

## Q16. What is a REST API?

A REST API is an HTTP-based interface that commonly uses methods such as GET, POST, PUT, PATCH, and DELETE to operate on resources.

## Q17. What is a Serializer?

A serializer converts complex data such as Django model instances into native Python data types that can be rendered as JSON. It can also validate incoming data.

## Q18. What is a ForeignKey?

A ForeignKey represents a many-to-one relationship between database models.

## Q19. What is `select_related()`?

`select_related()` uses SQL joins to retrieve related single-valued objects efficiently, reducing unnecessary database queries.

## Q20. What is `prefetch_related()`?

`prefetch_related()` retrieves related objects in separate queries and joins them in Python. It is useful for reverse foreign-key and many-to-many relationships.

## Q21. How does realtime stock updating work?

The backend retrieves stock prices from Finnhub. After receiving and validating new data, it saves the price and broadcasts an event through Django Channels. Connected frontend clients receive the update through WebSockets.

## Q22. Why use background tasks for stock updates?

Fetching external data can take time and may fail due to network or provider limitations. Background tasks keep these operations separate from normal API requests.

## Q23. How do you handle Finnhub API failures?

Use request timeouts, exception handling, retries with exponential backoff, rate-limit handling, logging, and appropriate fallback behavior.

## Q24. How do you protect user portfolio data?

Use authentication, object-level permission checks, and querysets filtered by the authenticated user. Never trust a user ID supplied by the client to determine ownership.

## Q25. How do you prevent duplicate watchlist entries?

Add a database-level unique constraint on the combination of user and stock. Also handle validation errors gracefully in the API.

## Q26. How do you calculate portfolio profit and loss?

Subtract the total invested amount from the current market value. For multiple purchases, calculate the weighted average purchase price or use a transaction-based accounting model.

## Q27. What is an OHLCV candle?

OHLCV represents Open, High, Low, Close, and Volume. It is commonly used to represent market price movement over a particular time interval.

## Q28. How do you test an external API integration?

Use mocked HTTP responses to test successful responses, invalid data, timeouts, provider errors, and rate-limit responses without depending on the live external service.

---

# 34. Important Technical Improvements

Before considering the project production-ready, address the following:

| Area | Required Improvement |
|---|---|
| Authentication | Complete registration, profile, password and token workflows |
| Authorization | Enforce user ownership for all private resources |
| Finnhub | Add rate-limit handling, retries and response validation |
| Stock updates | Use a shared service for fetching and saving quotes |
| Watchlist | Handle duplicate entries and database constraint errors |
| Portfolio | Implement complete CRUD and transaction history |
| Historical data | Store OHLCV candles with proper uniqueness constraints |
| Alerts | Implement reliable trigger and notification delivery |
| WebSockets | Validate subscriptions, permissions and reconnect behavior |
| Celery | Configure retries, monitoring and task failure handling |
| Database | Add indexes, constraints and query optimization |
| API | Add pagination, filtering, validation and documentation |
| Testing | Implement unit, API, integration and WebSocket tests |
| Deployment | Configure Docker, HTTPS, logging, backups and monitoring |

### Additional Design Recommendations

1. Use `DecimalField` for financial values instead of Python floating-point values.
2. Store timestamps in UTC and display them in the user's preferred timezone.
3. Keep historical snapshots separate from the latest stock quote.
4. Use database constraints to prevent duplicate records.
5. Use a transaction ledger for accurate portfolio accounting.
6. Use a shared quote service for both API and Celery workflows.
7. Do not expose external provider API keys to the frontend.
8. Use idempotent background tasks where possible.
9. Monitor API usage and external provider limits.
10. Keep market-data ingestion separate from user-facing API logic.

---

# 35. Final Project Checklist

## Project Setup

- [ ] Django project created.
- [ ] Virtual environment configured.
- [ ] Dependencies installed.
- [ ] Environment variables configured.
- [ ] PostgreSQL configured.
- [ ] Redis configured.

## Authentication

- [ ] User registration.
- [ ] JWT login.
- [ ] JWT refresh.
- [ ] User profile.
- [ ] Permissions.

## Stock Management

- [ ] Stock model.
- [ ] Stock price model.
- [ ] Finnhub integration.
- [ ] Stock list API.
- [ ] Stock search API.
- [ ] Latest price API.
- [ ] Manual refresh API.

## Watchlist

- [ ] Add stock.
- [ ] Remove stock.
- [ ] List watchlist.
- [ ] Prevent duplicates.

## Portfolio

- [ ] Add holding.
- [ ] Update holding.
- [ ] Remove holding.
- [ ] Portfolio summary.
- [ ] Profit and loss calculation.
- [ ] Transaction history.

## Realtime

- [ ] Django Channels installed.
- [ ] ASGI configured.
- [ ] Redis Channels layer configured.
- [ ] WebSocket consumer created.
- [ ] Stock updates broadcast.
- [ ] Frontend WebSocket connected.

## Background Tasks

- [ ] Celery configured.
- [ ] Celery worker running.
- [ ] Celery Beat configured.
- [ ] Stock update task implemented.
- [ ] Retry and error handling implemented.

## Historical Data

- [ ] OHLCV model created.
- [ ] Historical API integrated.
- [ ] Historical data saved.
- [ ] History API implemented.
- [ ] Chart.js integrated.

## Alerts and Notifications

- [ ] Price alert model.
- [ ] Alert CRUD APIs.
- [ ] Alert checking task.
- [ ] Notification model.
- [ ] In-app notifications.
- [ ] Email notifications.

## Final Quality

- [ ] Unit tests.
- [ ] API tests.
- [ ] WebSocket tests.
- [ ] Swagger documentation.
- [ ] Logging.
- [ ] Docker configuration.
- [ ] Production security settings.
- [ ] Deployment completed.

---

# 36. Conclusion

The Realtime Stock Market project is an advanced Django backend application that combines REST APIs, external financial data integration, background task processing, WebSocket communication, database management, and authentication.

It demonstrates practical backend development skills:

- Python and Django.
- Django REST Framework.
- PostgreSQL and database design.
- Third-party API integration.
- Redis and Celery.
- Django Channels and WebSockets.
- JWT authentication.
- Background processing.
- API testing.
- Docker and deployment.

The project is suitable for an intermediate-to-advanced backend development portfolio when the core features are implemented, tested, documented, and deployed.

**Important:** This documentation is a technical implementation guide, not a claim that every feature is already implemented. Complete the models, serializers, views, services, tasks, permissions, tests, and deployment configuration before describing the application as production-ready.

**Recommended implementation order:**

```text
Django Setup
     ↓
Authentication
     ↓
Database Models
     ↓
Finnhub Integration
     ↓
Stock REST APIs
     ↓
Watchlist
     ↓
Portfolio
     ↓
Redis + Celery
     ↓
Django Channels + WebSocket
     ↓
Historical Data + Charts
     ↓
Price Alerts + Notifications
     ↓
Testing + Docker + Deployment
```

**Final Goal:** Build a complete, secure, maintainable, and deployable realtime stock market application using Python and Django.
