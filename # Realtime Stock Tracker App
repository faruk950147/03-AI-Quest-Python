# Realtime Stock Tracker App
## Django + Finnhub API + Django Channels + Celery + Redis

একটি Realtime Stock Tracker Application তৈরি করব, যেখানে ব্যবহারকারী বিভিন্ন কোম্পানির Stock Price, Market News, Historical Chart, Watchlist এবং Price Alert দেখতে পারবে।

---

## 1. Project Overview

### Features

- Live / Near-real-time stock price updates
- Finnhub API integration
- Django REST Framework API
- Django Channels WebSocket
- Celery background tasks
- Redis message broker and channel layer
- Stock market news
- Historical stock price chart
- User authentication
- Personal watchlist
- Price alerts
- Bootstrap dashboard
- PostgreSQL database support

> Note: Finnhub REST API দিয়ে নির্দিষ্ট interval-এ price fetch করলে সেটি near-real-time polling। এটি exchange-level tick-by-tick streaming নয়।

---

## 2. Technology Stack

| Technology | Purpose |
|---|---|
| Python | Backend language |
| Django | Web framework |
| Django REST Framework | REST API |
| Finnhub API | Stock market data |
| Django Channels | WebSocket |
| Celery | Background task |
| Redis | Broker and channel layer |
| PostgreSQL | Database |
| Bootstrap 5 | Frontend UI |
| JavaScript | Frontend logic |
| Chart.js | Stock charts |

---

## 3. Project Architecture

```text
Browser
   |
   | HTTP Request
   v
Django + DRF
   |
   |----------------------|
   |                      |
   v                      v
PostgreSQL             Finnhub API
                          ^
                          |
                       Celery
                          |
                          v
                        Redis
                          |
                          v
                    Django Channels
                          |
                          v
                       WebSocket
                          |
                          v
                       Browser
```

### Data flow

1. Celery নির্দিষ্ট সময় পরপর Finnhub API call করবে।
2. Finnhub থেকে stock quote সংগ্রহ করবে।
3. Django database-এ price save করবে।
4. Redis-এর মাধ্যমে Channels group-এ update পাঠাবে।
5. WebSocket browser-এ নতুন price পাঠাবে।
6. JavaScript dashboard update করবে।

---

## 4. Project Structure

```text
realtime_stock_tracker/
│
├── config/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   ├── wsgi.py
│   └── celery.py
│
├── apps/
│   ├── stocks/
│   │   ├── migrations/
│   │   ├── management/
│   │   │   └── commands/
│   │   │       └── seed_stocks.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── services.py
│   │   ├── tasks.py
│   │   ├── consumers.py
│   │   ├── routing.py
│   │   └── admin.py
│   │
│   ├── watchlist/
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   └── urls.py
│   │
│   └── notifications/
│       ├── models.py
│       ├── tasks.py
│       └── services.py
│
├── templates/
│   └── dashboard.html
│
├── static/
│   ├── css/
│   │   └── dashboard.css
│   └── js/
│       └── dashboard.js
│
├── .env
├── .env.example
├── .gitignore
├── requirements.txt
└── manage.py
```

---

## 5. Environment Setup

### Create project

```bash
mkdir realtime_stock_tracker
cd realtime_stock_tracker

py -3.12 -m venv .venv
```

### Activate virtual environment (Windows)

```powershell
.venv\Scripts\Activate.ps1
```

### Install dependencies

Create `requirements.txt`:

```txt
Django>=5.2,<5.3
djangorestframework>=3.16,<3.17
channels[daphne]>=4.3,<5
channels-redis>=4.2,<5
celery[redis]>=5.5,<6
redis>=6,<7
httpx>=0.28,<1
psycopg[binary]>=3.2,<4
python-dotenv>=1,<2
```

Install:

```bash
pip install -r requirements.txt
```

### Create Django project

```bash
django-admin startproject config .
mkdir apps
python manage.py startapp stocks apps/stocks
```

অন্য app-গুলোও একইভাবে তৈরি করতে হবে। প্রয়োজনে package হিসেবে `apps/__init__.py` এবং প্রতিটি app folder-এ `__init__.py` রাখবে।

---

## 6. Finnhub API Setup

Website: https://finnhub.io/

1. Finnhub account তৈরি করো।
2. Dashboard থেকে API token সংগ্রহ করো।
3. Token কখনো frontend JavaScript-এ রাখবে না।
4. Token environment variable-এ রাখবে।

### .env

```env
SECRET_KEY=change-this-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

FINNHUB_API_KEY=your_finnhub_api_key

REDIS_URL=redis://127.0.0.1:6379/0

STOCK_POLL_SECONDS=60
```

### .gitignore

```gitignore
.env
.venv/
__pycache__/
*.pyc
db.sqlite3
staticfiles/
media/
```

---

## 7. Django Settings

### config/settings.py

প্রয়োজনীয় configuration:

```python
import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")

SECRET_KEY = os.getenv("SECRET_KEY", "development-only-key")
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

ALLOWED_HOSTS = os.getenv(
    "ALLOWED_HOSTS", "127.0.0.1,localhost"
).split(",")

INSTALLED_APPS = [
    "daphne",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "rest_framework",
    "channels",

    "apps.stocks",
    "apps.watchlist",
    "apps.notifications",
]

ASGI_APPLICATION = "config.asgi.application"

REDIS_URL = os.getenv(
    "REDIS_URL", "redis://127.0.0.1:6379/0"
)

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [REDIS_URL],
        },
    },
}

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
}

FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")
STOCK_POLL_SECONDS = int(
    os.getenv("STOCK_POLL_SECONDS", "60")
)

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
```

---

## 8. Database Models

### apps/stocks/models.py

```python
from django.db import models


class Stock(models.Model):
    symbol = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=150)
    exchange = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["symbol"]

    def __str__(self):
        return self.symbol


class StockPrice(models.Model):
    stock = models.ForeignKey(
        Stock,
        on_delete=models.CASCADE,
        related_name="prices"
    )

    current_price = models.DecimalField(
        max_digits=18, decimal_places=4
    )
    change = models.DecimalField(
        max_digits=18, decimal_places=4, default=0
    )
    percent_change = models.DecimalField(
        max_digits=10, decimal_places=4, default=0
    )

    high_price = models.DecimalField(
        max_digits=18, decimal_places=4, null=True, blank=True
    )
    low_price = models.DecimalField(
        max_digits=18, decimal_places=4, null=True, blank=True
    )
    open_price = models.DecimalField(
        max_digits=18, decimal_places=4, null=True, blank=True
    )
    previous_close = models.DecimalField(
        max_digits=18, decimal_places=4, null=True, blank=True
    )

    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-updated_at"]
        indexes = [
            models.Index(fields=["stock", "-updated_at"]),
        ]

    def __str__(self):
        return f"{self.stock.symbol}: {self.current_price}"


class MarketNews(models.Model):
    external_id = models.CharField(
        max_length=255, unique=True
    )
    headline = models.CharField(max_length=500)
    summary = models.TextField(blank=True)
    source = models.CharField(max_length=150, blank=True)
    url = models.URLField(max_length=1000)
    image = models.URLField(max_length=1000, blank=True)
    category = models.CharField(max_length=100, blank=True)
    published_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-published_at"]

    def __str__(self):
        return self.headline
```

### Watchlist model

`apps/watchlist/models.py`

```python
from django.conf import settings
from django.db import models
from apps.stocks.models import Stock


class WatchlistItem(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="watchlist_items"
    )
    stock = models.ForeignKey(
        Stock,
        on_delete=models.CASCADE
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

### Price Alert model

`apps/notifications/models.py`

```python
from django.conf import settings
from django.db import models
from apps.stocks.models import Stock


class PriceAlert(models.Model):
    ABOVE = "above"
    BELOW = "below"

    CONDITION_CHOICES = [
        (ABOVE, "Above"),
        (BELOW, "Below"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    stock = models.ForeignKey(
        Stock,
        on_delete=models.CASCADE
    )
    target_price = models.DecimalField(
        max_digits=18, decimal_places=4
    )
    condition = models.CharField(
        max_length=10,
        choices=CONDITION_CHOICES
    )
    is_triggered = models.BooleanField(default=False)
    triggered_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.stock.symbol} {self.condition} {self.target_price}"
```

---

## 9. Finnhub API Integration

### Important endpoints

| Endpoint | Purpose |
|---|---|
| /quote | Current stock quote |
| /stock/candle | Historical candles |
| /news | Market news |
| /stock/profile2 | Company profile |
| /search | Symbol search |

### Quote response fields

| Field | Meaning |
|---|---|
| c | Current price |
| d | Change |
| dp | Percent change |
| h | High price |
| l | Low price |
| o | Open price |
| pc | Previous close |
| t | Unix timestamp |

### apps/stocks/services.py

```python
import httpx
from django.conf import settings


class FinnhubError(Exception):
    pass


class FinnhubClient:

    BASE_URL = "https://finnhub.io/api/v1"

    def __init__(self):
        self.token = settings.FINNHUB_API_KEY

        if not self.token:
            raise FinnhubError("Finnhub API key is missing")

    def get(self, endpoint, params=None):
        params = params or {}
        params["token"] = self.token

        try:
            response = httpx.get(
                f"{self.BASE_URL}/{endpoint}",
                params=params,
                timeout=15
            )
            response.raise_for_status()
            data = response.json()

            if isinstance(data, dict) and data.get("error"):
                raise FinnhubError(data["error"])

            return data

        except httpx.HTTPError as exc:
            raise FinnhubError(str(exc)) from exc

    def quote(self, symbol):
        data = self.get(
            "quote",
            {"symbol": symbol}
        )

        if not data or not data.get("c"):
            raise FinnhubError(
                f"No quote available for {symbol}"
            )

        return data

    def market_news(self, category="general"):
        return self.get(
            "news",
            {"category": category}
        )

    def candles(self, symbol, resolution, start, end):
        return self.get(
            "stock/candle",
            {
                "symbol": symbol,
                "resolution": resolution,
                "from": start,
                "to": end,
            }
        )
```

---

## 10. Stock Serializers

### apps/stocks/serializers.py

```python
from rest_framework import serializers
from .models import Stock, StockPrice, MarketNews


class StockPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockPrice
        fields = [
            "current_price",
            "change",
            "percent_change",
            "high_price",
            "low_price",
            "open_price",
            "previous_close",
            "updated_at",
        ]


class StockSerializer(serializers.ModelSerializer):
    latest_price = serializers.SerializerMethodField()

    class Meta:
        model = Stock
        fields = [
            "id",
            "symbol",
            "name",
            "exchange",
            "latest_price",
        ]

    def get_latest_price(self, obj):
        price = obj.prices.first()

        if price:
            return StockPriceSerializer(price).data

        return None


class MarketNewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketNews
        fields = "__all__"
```

---

## 11. Stock API Views

### apps/stocks/views.py

```python
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Stock, MarketNews
from .serializers import StockSerializer, MarketNewsSerializer
from .services import FinnhubClient, FinnhubError


class StockListAPIView(generics.ListAPIView):
    queryset = Stock.objects.filter(is_active=True)
    serializer_class = StockSerializer


class StockDetailAPIView(generics.RetrieveAPIView):
    queryset = Stock.objects.filter(is_active=True)
    serializer_class = StockSerializer
    lookup_field = "symbol"


class NewsListAPIView(generics.ListAPIView):
    queryset = MarketNews.objects.all()
    serializer_class = MarketNewsSerializer


class RefreshStockAPIView(APIView):

    def post(self, request, symbol):
        try:
            stock = Stock.objects.get(
                symbol=symbol.upper(),
                is_active=True
            )

            data = FinnhubClient().quote(stock.symbol)

            return Response({
                "symbol": stock.symbol,
                "quote": data,
            })

        except Stock.DoesNotExist:
            return Response(
                {"error": "Stock not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        except FinnhubError as exc:
            return Response(
                {"error": str(exc)},
                status=status.HTTP_502_BAD_GATEWAY
            )
```

### apps/stocks/urls.py

```python
from django.urls import path
from .views import (
    StockListAPIView,
    StockDetailAPIView,
    NewsListAPIView,
    RefreshStockAPIView,
)

urlpatterns = [
    path("", StockListAPIView.as_view(), name="stock-list"),
    path("<str:symbol>/", StockDetailAPIView.as_view(), name="stock-detail"),
    path(
        "<str:symbol>/refresh/",
        RefreshStockAPIView.as_view(),
        name="stock-refresh"
    ),
    path("news/", NewsListAPIView.as_view(), name="news-list"),
]
```

### config/urls.py

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/stocks/", include("apps.stocks.urls")),
]
```

---

## 12. Celery Configuration

### config/celery.py

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

### config/__init__.py

```python
from .celery import app as celery_app

__all__ = ("celery_app",)
```

### Add to settings.py

```python
CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = REDIS_URL

CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"

CELERY_TIMEZONE = "Asia/Dhaka"

CELERY_BEAT_SCHEDULE = {
    "refresh-stock-prices": {
        "task": "apps.stocks.tasks.refresh_stock_quotes",
        "schedule": STOCK_POLL_SECONDS,
    },
}
```

---

## 13. Celery Stock Price Task

### apps/stocks/tasks.py

```python
from decimal import Decimal
from celery import shared_task
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from .models import Stock, StockPrice
from .services import FinnhubClient, FinnhubError


@shared_task
def refresh_stock_quotes():

    client = FinnhubClient()
    channel_layer = get_channel_layer()

    stocks = Stock.objects.filter(is_active=True)

    for stock in stocks:
        try:
            quote = client.quote(stock.symbol)

            price = StockPrice.objects.create(
                stock=stock,
                current_price=Decimal(str(quote["c"])),
                change=Decimal(str(quote.get("d") or 0)),
                percent_change=Decimal(str(quote.get("dp") or 0)),
                high_price=Decimal(str(quote.get("h") or 0)),
                low_price=Decimal(str(quote.get("l") or 0)),
                open_price=Decimal(str(quote.get("o") or 0)),
                previous_close=Decimal(str(quote.get("pc") or 0)),
            )

            payload = {
                "symbol": stock.symbol,
                "name": stock.name,
                "current_price": str(price.current_price),
                "change": str(price.change),
                "percent_change": str(price.percent_change),
                "updated_at": price.updated_at.isoformat(),
            }

            async_to_sync(channel_layer.group_send)(
                "stock_updates",
                {
                    "type": "stock.price",
                    "data": payload,
                }
            )

        except FinnhubError as exc:
            print(f"Finnhub error for {stock.symbol}: {exc}")

        except Exception as exc:
            print(f"Unexpected error for {stock.symbol}: {exc}")
```

Production-এর জন্য logging, rate-limit handling, retry/backoff, task locking এবং duplicate task prevention যোগ করতে হবে।

---

## 14. Django Channels WebSocket

### apps/stocks/consumers.py

```python
import json
from channels.generic.websocket import AsyncWebsocketConsumer


class StockConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.group_name = "stock_updates"

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

    async def stock_price(self, event):
        await self.send(
            text_data=json.dumps({
                "type": "stock_update",
                "data": event["data"],
            })
        )
```

### apps/stocks/routing.py

```python
from django.urls import path
from .consumers import StockConsumer

websocket_urlpatterns = [
    path(
        "ws/stocks/",
        StockConsumer.as_asgi()
    ),
]
```

### config/asgi.py

```python
import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "config.settings"
)

django_asgi_app = get_asgi_application()

from apps.stocks.routing import websocket_urlpatterns

application = ProtocolTypeRouter({
    "http": django_asgi_app,

    "websocket": AuthMiddlewareStack(
        URLRouter(websocket_urlpatterns)
    ),
})
```

Production-এ WebSocket origin validation, authentication, authorization এবং private group access ঠিকভাবে configure করতে হবে।

---

## 15. Historical Stock Data

Finnhub endpoint:

```text
GET /stock/candle
```

Parameters:

| Parameter | Meaning |
|---|---|
| symbol | Stock symbol |
| resolution | Candle interval |
| from | Start Unix timestamp |
| to | End Unix timestamp |
| token | API key |

Response:

- c = Close
- h = High
- l = Low
- o = Open
- t = Timestamp
- v = Volume

Example Python:

```python
import time
from datetime import datetime, timezone

from apps.stocks.services import FinnhubClient

end = int(time.time())
start = end - (7 * 24 * 60 * 60)

client = FinnhubClient()

data = client.candles(
    symbol="AAPL",
    resolution="D",
    start=start,
    end=end,
)

if data.get("s") == "ok":
    for timestamp, close in zip(data["t"], data["c"]):
        date = datetime.fromtimestamp(
            timestamp,
            tz=timezone.utc
        )
        print(date, close)
```

---

## 16. Market News Integration

Finnhub news endpoint:

```text
GET /news?category=general
```

Example:

```python
from datetime import datetime, timezone as dt_timezone

from apps.stocks.services import FinnhubClient
from apps.stocks.models import MarketNews


def sync_market_news():
    client = FinnhubClient()
    articles = client.market_news("general")

    for article in articles:
        external_id = str(
            article.get("id") or article.get("url")
        )

        if not external_id:
            continue

        published = article.get("datetime")

        published_at = (
            datetime.fromtimestamp(
                published,
                tz=dt_timezone.utc
            )
            if published else None
        )

        MarketNews.objects.update_or_create(
            external_id=external_id,
            defaults={
                "headline": article.get("headline", ""),
                "summary": article.get("summary", ""),
                "source": article.get("source", ""),
                "url": article.get("url", ""),
                "image": article.get("image", ""),
                "category": article.get("category", ""),
                "published_at": published_at,
            }
        )
```

News sync-ও Celery task হিসেবে schedule করা যায়।

---

## 17. Watchlist API

### apps/watchlist/serializers.py

```python
from rest_framework import serializers
from .models import WatchlistItem


class WatchlistSerializer(serializers.ModelSerializer):
    symbol = serializers.CharField(
        source="stock.symbol",
        read_only=True
    )
    name = serializers.CharField(
        source="stock.name",
        read_only=True
    )

    class Meta:
        model = WatchlistItem
        fields = ["id", "stock", "symbol", "name", "created_at"]
        read_only_fields = ["id", "created_at"]
```

### apps/watchlist/views.py

```python
from rest_framework import generics, serializers
from rest_framework.permissions import IsAuthenticated

from apps.stocks.models import Stock
from .models import WatchlistItem
from .serializers import WatchlistSerializer


class WatchlistListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = WatchlistSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return WatchlistItem.objects.filter(
            user=self.request.user
        ).select_related("stock")

    def perform_create(self, serializer):
        stock_id = self.request.data.get("stock")

        try:
            stock = Stock.objects.get(
                pk=stock_id,
                is_active=True
            )
        except (Stock.DoesNotExist, ValueError, TypeError):
            raise serializers.ValidationError({
                "stock": "Valid active stock is required."
            })

        serializer.save(
            user=self.request.user,
            stock=stock
        )


class WatchlistDeleteAPIView(generics.DestroyAPIView):
    serializer_class = WatchlistSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return WatchlistItem.objects.filter(
            user=self.request.user
        )
```

### apps/watchlist/urls.py

```python
from django.urls import path
from .views import (
    WatchlistListCreateAPIView,
    WatchlistDeleteAPIView,
)

urlpatterns = [
    path(
        "",
        WatchlistListCreateAPIView.as_view(),
        name="watchlist-list-create"
    ),
    path(
        "<int:pk>/",
        WatchlistDeleteAPIView.as_view(),
        name="watchlist-delete"
    ),
]
```

Root URL configuration-এ যোগ করো:

```python
path("api/watchlist/", include("apps.watchlist.urls")),
```

---

## 18. Price Alert Logic

### apps/notifications/tasks.py

```python
from django.utils import timezone
from celery import shared_task

from .models import PriceAlert
from apps.stocks.models import StockPrice


@shared_task
def check_price_alerts():

    alerts = PriceAlert.objects.filter(
        is_triggered=False
    ).select_related("stock")

    for alert in alerts:

        latest_price = StockPrice.objects.filter(
            stock=alert.stock
        ).first()

        if not latest_price:
            continue

        current = latest_price.current_price
        target = alert.target_price

        triggered = (
            alert.condition == "above" and current >= target
        ) or (
            alert.condition == "below" and current <= target
        )

        if triggered:
            alert.is_triggered = True
            alert.triggered_at = timezone.now()
            alert.save(
                update_fields=["is_triggered", "triggered_at"]
            )
```

Production-এ একই alert একাধিক worker থেকে trigger হওয়া ঠেকাতে atomic database update/locking ব্যবহার করতে হবে। Email বা in-app notification-ও যুক্ত করা যাবে।

---

## 19. Seed Stock Data

### apps/stocks/management/commands/seed_stocks.py

```python
from django.core.management.base import BaseCommand
from apps.stocks.models import Stock


class Command(BaseCommand):
    help = "Create initial stock symbols"

    def handle(self, *args, **kwargs):

        stocks = [
            ("AAPL", "Apple Inc."),
            ("MSFT", "Microsoft Corporation"),
            ("NVDA", "NVIDIA Corporation"),
            ("TSLA", "Tesla Inc."),
            ("AMZN", "Amazon.com Inc."),
            ("GOOGL", "Alphabet Inc."),
            ("META", "Meta Platforms Inc."),
            ("NFLX", "Netflix Inc."),
        ]

        for symbol, name in stocks:
            Stock.objects.update_or_create(
                symbol=symbol,
                defaults={"name": name}
            )

        self.stdout.write(
            self.style.SUCCESS("Stocks seeded successfully")
        )
```

Run:

```bash
python manage.py seed_stocks
```

---

## 20. Frontend Dashboard

### templates/dashboard.html

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Stock Tracker</title>

    <link
        href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css"
        rel="stylesheet"
    >
</head>

<body class="bg-light">

<div class="container py-5">

    <h2 class="mb-4">Realtime Stock Tracker</h2>

    <div class="mb-3">
        WebSocket:
        <span id="connection-status" class="badge text-bg-secondary">
            Connecting...
        </span>
    </div>

    <div class="card shadow-sm">
        <div class="card-body">

            <table class="table table-hover">
                <thead>
                    <tr>
                        <th>Symbol</th>
                        <th>Company</th>
                        <th>Price</th>
                        <th>Change</th>
                        <th>Updated</th>
                    </tr>
                </thead>

                <tbody id="stock-table-body">
                    <tr>
                        <td colspan="5">Loading stocks...</td>
                    </tr>
                </tbody>
            </table>

        </div>
    </div>

</div>

<script src="/static/js/dashboard.js"></script>
</body>
</html>
```

### static/js/dashboard.js

```javascript
const tableBody = document.getElementById("stock-table-body");
const statusElement = document.getElementById("connection-status");

const rows = new Map();

function createCell(text) {
    const td = document.createElement("td");
    td.textContent = text ?? "-";
    return td;
}

function renderStock(stock) {
    let row = rows.get(stock.symbol);

    if (!row) {
        row = document.createElement("tr");
        rows.set(stock.symbol, row);
        tableBody.appendChild(row);
    }

    row.replaceChildren(
        createCell(stock.symbol),
        createCell(stock.name),
        createCell(stock.current_price),
        createCell(stock.percent_change + "%"),
        createCell(stock.updated_at)
    );
}

async function loadStocks() {
    const response = await fetch("/api/stocks/");

    if (!response.ok) {
        throw new Error("Unable to load stocks");
    }

    const stocks = await response.json();

    tableBody.replaceChildren();

    stocks.forEach(stock => {
        const latest = stock.latest_price;

        if (!latest) return;

        renderStock({
            symbol: stock.symbol,
            name: stock.name,
            current_price: latest.current_price,
            percent_change: latest.percent_change,
            updated_at: latest.updated_at
        });
    });
}

function connectWebSocket() {
    const protocol = location.protocol === "https:" ? "wss" : "ws";

    const socket = new WebSocket(
        protocol + "://" + location.host + "/ws/stocks/"
    );

    socket.onopen = () => {
        statusElement.textContent = "Connected";
        statusElement.className = "badge text-bg-success";
    };

    socket.onmessage = event => {
        const message = JSON.parse(event.data);

        if (message.type === "stock_update") {
            renderStock(message.data);
        }
    };

    socket.onclose = () => {
        statusElement.textContent = "Disconnected";
        statusElement.className = "badge text-bg-danger";

        setTimeout(connectWebSocket, 3000);
    };

    socket.onerror = () => {
        socket.close();
    };
}

loadStocks()
    .catch(console.error);

connectWebSocket();
```

### Frontend security

- User-provided content সরাসরি innerHTML-এ বসাবে না।
- DOM update করতে textContent ব্যবহার করবে।
- API key frontend-এ প্রকাশ করবে না।
- Authentication থাকলে CSRF ও permission ঠিকভাবে configure করবে।

---

## 21. Redis Setup

Docker দিয়ে Redis চালানো:

```bash
docker run --name stock-redis -p 6379:6379 -d redis:7
```

Check:

```bash
docker exec -it stock-redis redis-cli ping
```

Expected:

```text
PONG
```

---

## 22. Database Migration

```bash
python manage.py makemigrations
python manage.py migrate
```

Create admin user:

```bash
python manage.py createsuperuser
```

Run Django:

```bash
python manage.py runserver
```

---

## 23. Start Celery Worker

একটি নতুন terminal:

Windows:

```powershell
celery -A config worker -l info -P solo
```

Linux/macOS:

```bash
celery -A config worker -l info
```

---

## 24. Start Celery Beat

আরেকটি terminal:

```bash
celery -A config beat -l info
```

Beat নির্দিষ্ট interval-এ task schedule করবে।

---

## 25. Test Celery Task Manually

```bash
python manage.py shell
```

```python
from apps.stocks.tasks import refresh_stock_quotes

refresh_stock_quotes.delay()
```

---

## 26. API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | /api/stocks/ | Stock list |
| GET | /api/stocks/AAPL/ | Stock details |
| POST | /api/stocks/AAPL/refresh/ | Manual refresh |
| GET | /api/stocks/news/ | Market news |
| GET | /api/watchlist/ | User watchlist |
| POST | /api/watchlist/ | Add watchlist item |
| DELETE | /api/watchlist/1/ | Remove watchlist item |

WebSocket:

```text
ws://127.0.0.1:8000/ws/stocks/
```

HTTPS production:

```text
wss://your-domain.com/ws/stocks/
```

---

## 27. Testing Checklist

### Backend

- [ ] Django server starts successfully
- [ ] Database migrations work
- [ ] Stock model saves correctly
- [ ] Finnhub API key works
- [ ] Quote endpoint returns data
- [ ] News endpoint returns data
- [ ] Stock API returns JSON
- [ ] Watchlist requires authentication
- [ ] User cannot delete another user's watchlist
- [ ] Price alerts trigger only once

### Celery

- [ ] Redis connection works
- [ ] Worker starts
- [ ] Beat starts
- [ ] Stock refresh task executes
- [ ] Stock prices save to database
- [ ] API rate limits are handled

### WebSocket

- [ ] WebSocket connects
- [ ] Consumer joins group
- [ ] Celery broadcasts updates
- [ ] Browser receives updates
- [ ] Reconnect works after disconnection

### Frontend

- [ ] Dashboard loads
- [ ] Stock rows display
- [ ] Price updates dynamically
- [ ] Connection status displays
- [ ] No unsafe HTML injection

---

## 28. Production Improvements

Production deployment-এর আগে:

1. DEBUG=False
2. Strong SECRET_KEY
3. PostgreSQL database
4. Redis password and private network
5. HTTPS and WSS
6. WebSocket authentication and origin validation
7. Finnhub rate-limit handling
8. Celery retry/backoff
9. Logging and monitoring
10. Database indexes
11. Pagination for API
12. Environment-based configuration
13. Automated tests
14. Gunicorn/Uvicorn/Daphne deployment
15. Static file serving
16. Backup strategy

---

## 29. Common Problems

### Redis connection refused

কারণ: Redis চালু নেই অথবা URL ভুল।

সমাধান:

```bash
docker start stock-redis
```

### Finnhub API key missing

সমাধান:
- .env file check করো।
- settings.py-তে load_dotenv আছে কি না দেখো।
- Server restart করো।

### WebSocket 404

Check:
- ASGI_APPLICATION
- config/asgi.py
- apps/stocks/routing.py
- URL path

### Celery task run হচ্ছে না

Check:
- Redis
- Worker
- Celery Beat
- Task autodiscovery
- Task import path

### Stock price update হচ্ছে না

Check:
- API token
- Finnhub response
- Stock is_active=True
- Celery logs
- API rate limit

---

## 30. Learning Roadmap

### Phase 1: Django Basics
- Models
- Views
- URLs
- Templates
- ORM
- Authentication

### Phase 2: REST API
- DRF serializers
- API views
- Generic views
- Permissions
- Authentication

### Phase 3: External API
- HTTP requests
- Finnhub integration
- API errors
- Rate limits
- Response parsing

### Phase 4: Background Tasks
- Celery
- Redis broker
- Celery Beat
- Retry and scheduling

### Phase 5: Realtime
- ASGI
- Django Channels
- WebSocket
- Channel layers
- Group broadcasting

### Phase 6: Frontend
- Bootstrap
- JavaScript Fetch
- WebSocket client
- Chart.js

### Phase 7: Production
- PostgreSQL
- Docker
- Deployment
- Security
- Monitoring

---

## 31. Interview Questions

1. What is Django REST Framework?
2. What is the difference between HTTP and WebSocket?
3. What is ASGI?
4. What is Django Channels?
5. What is Redis?
6. What is Celery?
7. What is Celery Beat?
8. What is the difference between Celery Worker and Beat?
9. How do you integrate an external API?
10. How do you handle API rate limits?
11. What is the purpose of a serializer?
12. What is select_related()?
13. What is prefetch_related()?
14. How do you protect an API key?
15. How do you authenticate a WebSocket connection?
16. How do you prevent duplicate Celery tasks?
17. How do you store historical stock prices?
18. How do you test asynchronous tasks?

---

## 32. Important Concepts

### HTTP vs WebSocket

HTTP:
- Request/response model
- Client requests data
- Server returns response

WebSocket:
- Persistent connection
- Two-way communication
- Server can push updates

### Celery vs Django Channels

Celery:
- Background jobs
- Scheduled tasks
- API polling
- Email processing

Django Channels:
- WebSocket
- Realtime browser updates
- Event broadcasting

### Redis

Redis ব্যবহার হয়:
- Celery broker
- Celery result backend
- Channels layer
- Temporary cache

---

## 33. Final Project Checklist

- [ ] Project setup
- [ ] Dependencies installed
- [ ] Finnhub API key configured
- [ ] Django settings configured
- [ ] Stock models created
- [ ] Database migrated
- [ ] Finnhub service created
- [ ] Stock API completed
- [ ] News API completed
- [ ] Celery configured
- [ ] Redis configured
- [ ] Celery Beat configured
- [ ] Channels configured
- [ ] WebSocket consumer created
- [ ] Dashboard created
- [ ] Watchlist completed
- [ ] Price alert completed
- [ ] Historical chart completed
- [ ] Tests written
- [ ] Production deployment completed

---

## 34. Official Documentation

- Django: https://docs.djangoproject.com/
- Django REST Framework: https://www.django-rest-framework.org/
- Django Channels: https://channels.readthedocs.io/
- Celery: https://docs.celeryq.dev/
- Redis: https://redis.io/docs/
- Finnhub: https://finnhub.io/docs/api
- Bootstrap: https://getbootstrap.com/docs/
- Chart.js: https://www.chartjs.org/docs/

---

## Final Note

এই README হলো project-এর architecture, learning notes এবং implementation guide। এখানে দেখানো snippets একত্র করলেই সম্পূর্ণ tested production application তৈরি হয়ে যায় না। বিশেষ করে URL configuration, authentication, historical chart API, alert CRUD, automated tests এবং deployment আলাদাভাবে সম্পূর্ণ ও পরীক্ষা করতে হবে।
