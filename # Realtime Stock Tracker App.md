# Realtime Stock Tracker – Complete Django Project Documentation

**Project Type:** Advanced Python Django Backend Project  
**Project Name:** Realtime Stock Tracker  
**Backend:** Python, Django, Django REST Framework  
**External API:** Finnhub Stock Market API  
**Realtime Communication:** Django Channels + WebSocket  
**Background Processing:** Celery + Celery Beat  
**Message Broker:** Redis  
**Database:** PostgreSQL / SQLite (Development)  
**Frontend:** HTML, CSS, Bootstrap 5, JavaScript  
**Charts:** Chart.js  
**HTTP Client:** HTTPX  

---

# Table of Contents

1. Project Overview
2. Project Objectives
3. Main Features
4. Technology Stack
5. Project Architecture
6. Complete Project Structure
7. Development Environment Setup
8. Dependencies
9. Environment Variables
10. Django Project Configuration
11. Database Configuration
12. Database Models
13. User Authentication
14. Finnhub API Integration
15. Stock Serializers
16. Stock REST API
17. Portfolio Management
18. Watchlist Management
19. Historical Stock Data
20. Market News
21. Celery Configuration
22. Celery Background Tasks
23. Redis Configuration
24. Django Channels Configuration
25. WebSocket Consumer
26. Price Alert System
27. Frontend Dashboard
28. JavaScript WebSocket Client
29. API Endpoints
30. HTTP Status Codes
31. Security Implementation
32. Error Handling
33. Database Migrations
34. Running the Project
35. Testing Strategy
36. Common Problems and Solutions
37. Performance Optimization
38. Production Deployment
39. Git and GitHub
40. Development Roadmap
41. Interview Questions and Answers
42. Important Backend Concepts
43. Final Project Checklist
44. Official Documentation

---

# 1. Project Overview

Realtime Stock Tracker is a Django-based web application that allows users to monitor stock market information through a dynamic dashboard.

Users can search for stocks, add stocks to their personal portfolio or watchlist, view current prices, analyze historical price charts, read market news, and configure price alerts.

The application uses Finnhub API to retrieve stock market information.

Celery periodically retrieves stock quotes in the background. Django Channels and WebSocket distribute updated prices to connected browsers without requiring a full page reload.

**Important:** When prices are fetched periodically through Finnhub REST API, the system provides near-real-time updates, not guaranteed exchange-level tick-by-tick streaming.

## Project Workflow

1. A user registers and logs in.
2. The user opens the stock dashboard.
3. The dashboard loads stock information through Django REST Framework.
4. The user adds stocks to a portfolio or watchlist.
5. Celery periodically fetches stock prices from Finnhub.
6. Updated prices are stored in the database.
7. Redis and Django Channels distribute updates through WebSocket.
8. JavaScript receives the updates.
9. The dashboard displays the latest available prices.
10. Price alerts are checked in the background.

---

# 2. Project Objectives

The main objectives are:

- Build a complete Django backend application.
- Understand Django ORM and database relationships.
- Integrate an external financial API.
- Develop RESTful APIs using Django REST Framework.
- Implement secure user authentication.
- Understand asynchronous background processing.
- Implement WebSocket communication.
- Use Redis as a message broker and channel layer.
- Create scheduled tasks using Celery Beat.
- Build a dynamic JavaScript dashboard.
- Store historical stock prices.
- Implement user-specific portfolios and watchlists.
- Create a price alert notification system.
- Learn production-level backend architecture.

---

# 3. Main Features

## A. User Management

- User registration
- User login
- User logout
- Password validation
- Session authentication
- User-specific data access

## B. Stock Management

- Stock listing
- Stock search
- Stock details
- Add stock to portfolio
- Remove stock from portfolio
- View current stock price
- View price changes
- Refresh stock information

## C. Market Information

- Current stock quotes
- Opening price
- Highest price
- Lowest price
- Previous closing price
- Price change
- Percentage change
- Historical stock data
- Market news
- Company information

## D. Realtime Features

- WebSocket connection
- Live dashboard updates
- Automatic reconnection
- Connection status
- Background price updates

## E. Watchlist

- Add stock to watchlist
- Remove stock from watchlist
- View personal watchlist
- Prevent duplicate watchlist entries

## F. Price Alerts

- Set target price
- Alert when price goes above target
- Alert when price goes below target
- Trigger alert once
- Store alert history
- In-app or email notification

## G. Security

- Authentication
- Authorization
- CSRF protection
- API key protection
- Rate limiting
- Input validation
- WebSocket origin validation
- User-specific database queries

---

# 4. Technology Stack

| Technology | Purpose |
|---|---|
| Python | Backend programming language |
| Django | Web framework |
| Django REST Framework | REST API development |
| Finnhub API | Stock market data |
| HTTPX | External HTTP requests |
| Django Channels | WebSocket communication |
| ASGI | Asynchronous server interface |
| Celery | Background task processing |
| Celery Beat | Scheduled task execution |
| Redis | Celery broker and Channels layer |
| PostgreSQL | Production database |
| SQLite | Development database |
| HTML | Page structure |
| CSS | Page styling |
| Bootstrap 5 | Responsive UI |
| JavaScript | Frontend logic |
| Fetch API | HTTP communication |
| Chart.js | Historical price charts |

---

# 5. Project Architecture

## High-Level Architecture

```text
                         USER
                           |
                           v
                       BROWSER
                           |
                 ---------------------
                 |                   |
                 v                   v
             HTTP / REST         WebSocket
                 |                   |
                 v                   v
             DJANGO + DRF       DJANGO CHANNELS
                 |                   ^
                 |                   |
          ----------------           |
          |              |           |
          v              v           |
      PostgreSQL      Finnhub API    |
                         ^           |
                         |           |
                       CELERY        |
                         |           |
                         v           |
                       REDIS --------
                         |
                         v
                    CELERY BEAT
```

## Detailed Data Flow

### Stock Price Update

```text
Celery Beat
    |
    v
Celery Worker
    |
    v
Finnhub REST API
    |
    v
Stock Quote Response
    |
    v
Django Service Layer
    |
    v
PostgreSQL
    |
    v
Redis Channel Layer
    |
    v
Django Channels
    |
    v
WebSocket
    |
    v
JavaScript Dashboard
```

### Important Responsibilities

**Django:**
- Handles HTTP requests.
- Manages authentication.
- Provides application logic.
- Interacts with the database.

**DRF:**
- Provides REST APIs.
- Serializes model data.
- Handles API validation.
- Controls API permissions.

**Celery:**
- Executes background tasks.
- Fetches external stock data.
- Checks price alerts.
- Synchronizes market news.

**Celery Beat:**
- Schedules recurring tasks.

**Redis:**
- Acts as Celery message broker.
- Stores Celery task results when configured.
- Provides Channels message transport.
- Can also be used for caching.

**Django Channels:**
- Manages WebSocket connections.
- Broadcasts stock updates.

**Finnhub:**
- Supplies external market data.

---

# 6. Complete Project Structure

```text
realtime_stock_tracker/
│
├── manage.py
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
│   ├── __init__.py
│   │
│   ├── accounts/
│   │   ├── migrations/
│   │   ├── __init__.py
│   │   ├── apps.py
│   │   ├── forms.py
│   │   ├── views.py
│   │   └── urls.py
│   │
│   ├── stocks/
│   │   ├── migrations/
│   │   ├── management/
│   │   │   ├── __init__.py
│   │   │   └── commands/
│   │   │       ├── __init__.py
│   │   │       └── seed_stocks.py
│   │   ├── __init__.py
│   │   ├── apps.py
│   │   ├── admin.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── services.py
│   │   ├── tasks.py
│   │   ├── consumers.py
│   │   └── routing.py
│   │
│   ├── portfolio/
│   │   ├── migrations/
│   │   ├── __init__.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   └── urls.py
│   │
│   ├── watchlist/
│   │   ├── migrations/
│   │   ├── __init__.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   └── urls.py
│   │
│   └── notifications/
│       ├── migrations/
│       ├── __init__.py
│       ├── apps.py
│       ├── models.py
│       ├── tasks.py
│       ├── services.py
│       ├── serializers.py
│       ├── views.py
│       └── urls.py
│
├── templates/
│   ├── base.html
│   ├── dashboard.html
│   ├── login.html
│   └── register.html
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
└── README.md
```

### App Responsibilities

| App | Responsibility |
|---|---|
| accounts | User registration and authentication |
| stocks | Stock models, API, Finnhub and realtime updates |
| portfolio | User-specific stock portfolio |
| watchlist | Personal watchlist |
| notifications | Price alerts and notifications |

---

# 7. Development Environment Setup

## Step 1: Create Project Folder

```bash
mkdir realtime_stock_tracker
cd realtime_stock_tracker
```

## Step 2: Create Virtual Environment

Windows:

```powershell
py -3.12 -m venv .venv
```

Activate:

```powershell
.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use:

```cmd
.venv\Scripts\activate.bat
```

## Step 3: Install Dependencies

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
django-ratelimit>=4,<5
```

Install:

```bash
pip install -r requirements.txt
```

Save installed versions:

```bash
pip freeze > requirements-lock.txt
```

## Step 4: Create Django Project

```bash
django-admin startproject config .
```

Create app package:

```bash
mkdir apps
```

Create Python package file:

```text
apps/__init__.py
```

Create applications:

```bash
python manage.py startapp accounts apps/accounts
python manage.py startapp stocks apps/stocks
python manage.py startapp portfolio apps/portfolio
python manage.py startapp watchlist apps/watchlist
python manage.py startapp notifications apps/notifications
```

Ensure every application directory contains its `__init__.py` file.

---

# 8. Finnhub API Setup

Website:

https://finnhub.io/

## Setup Process

1. Create a Finnhub account.
2. Open the Finnhub dashboard.
3. Generate an API token.
4. Copy the token.
5. Store it in the `.env` file.
6. Never expose the token in frontend JavaScript.
7. Never upload the actual token to GitHub.

## Important Finnhub Endpoints

| Endpoint | Purpose |
|---|---|
| `/quote` | Current stock quote |
| `/stock/candle` | Historical stock prices |
| `/news` | Market news |
| `/stock/profile2` | Company profile |
| `/search` | Stock symbol search |

## Quote Response Fields

| Field | Meaning |
|---|---|
| c | Current price |
| d | Price change |
| dp | Percentage change |
| h | High price |
| l | Low price |
| o | Open price |
| pc | Previous close |
| t | Unix timestamp |

---

# 9. Environment Variables

Create `.env`:

```env
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

FINNHUB_API_KEY=your_finnhub_api_key

REDIS_URL=redis://127.0.0.1:6379/0

DB_NAME=stock_tracker
DB_USER=postgres
DB_PASSWORD=your_database_password
DB_HOST=127.0.0.1
DB_PORT=5432

STOCK_POLL_SECONDS=60
```

Create `.env.example`:

```env
SECRET_KEY=
DEBUG=False
ALLOWED_HOSTS=

FINNHUB_API_KEY=

REDIS_URL=

DB_NAME=
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=
```

## .gitignore

```gitignore
.env
.venv/
__pycache__/
*.py[cod]
db.sqlite3
staticfiles/
media/
.pytest_cache/
.coverage
```

---

# 10. Django Project Configuration

## config/settings.py

```python
import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")

SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "development-only-secret-key"
)

DEBUG = os.getenv(
    "DEBUG", "False"
).lower() == "true"

ALLOWED_HOSTS = [
    host.strip()
    for host in os.getenv(
        "ALLOWED_HOSTS",
        "127.0.0.1,localhost"
    ).split(",")
    if host.strip()
]

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

    "apps.accounts",
    "apps.stocks",
    "apps.portfolio",
    "apps.watchlist",
    "apps.notifications",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

# Development database: SQLite

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Production PostgreSQL example:
#
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql",
#         "NAME": os.getenv("DB_NAME"),
#         "USER": os.getenv("DB_USER"),
#         "PASSWORD": os.getenv("DB_PASSWORD"),
#         "HOST": os.getenv("DB_HOST"),
#         "PORT": os.getenv("DB_PORT", "5432"),
#     }
# }

REDIS_URL = os.getenv(
    "REDIS_URL",
    "redis://127.0.0.1:6379/0"
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
        "rest_framework.permissions.IsAuthenticated",
    ],
}

FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")

STOCK_POLL_SECONDS = int(
    os.getenv("STOCK_POLL_SECONDS", "60")
)

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

LOGIN_URL = "/login/"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/login/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Celery

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
    "check-price-alerts": {
        "task": "apps.notifications.tasks.check_price_alerts",
        "schedule": 60.0,
    },
    "sync-market-news": {
        "task": "apps.stocks.tasks.sync_market_news_task",
        "schedule": 300.0,
    },
}

```

**Note:** Production-এর জন্য PostgreSQL configuration সক্রিয় করতে হবে। REST Framework-এর default permission এখানে authenticated রাখা হয়েছে। যেসব stock/news endpoint public করতে চাও, সেগুলোতে আলাদাভাবে `AllowAny` ব্যবহার করবে।

---

# 11. Database Models

এই project-এ প্রধানত পাঁচটি database entity ব্যবহার করা হবে:

1. Stock
2. StockPrice
3. Portfolio
4. WatchlistItem
5. PriceAlert

MarketNews-এর জন্য আরেকটি model থাকবে।

## A. Stock Model

File: `apps/stocks/models.py`

```python
from django.db import models


class Stock(models.Model):

    symbol = models.CharField(
        max_length=20,
        unique=True
    )

    name = models.CharField(
        max_length=150
    )

    exchange = models.CharField(
        max_length=100,
        blank=True
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["symbol"]

    def __str__(self):
        return self.symbol
```

### Explanation

- `symbol`: Stock ticker, such as AAPL.
- `name`: Company name.
- `exchange`: Stock exchange.
- `is_active`: Determines whether the stock is available.
- `created_at`: Record creation time.

## B. StockPrice Model

```python
class StockPrice(models.Model):

    stock = models.ForeignKey(
        Stock,
        on_delete=models.CASCADE,
        related_name="prices"
    )

    current_price = models.DecimalField(
        max_digits=18,
        decimal_places=4
    )

    change = models.DecimalField(
        max_digits=18,
        decimal_places=4,
        default=0
    )

    percent_change = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        default=0
    )

    high_price = models.DecimalField(
        max_digits=18,
        decimal_places=4,
        null=True,
        blank=True
    )

    low_price = models.DecimalField(
        max_digits=18,
        decimal_places=4,
        null=True,
        blank=True
    )

    open_price = models.DecimalField(
        max_digits=18,
        decimal_places=4,
        null=True,
        blank=True
    )

    previous_close = models.DecimalField(
        max_digits=18,
        decimal_places=4,
        null=True,
        blank=True
    )

    market_timestamp = models.DateTimeField(
        null=True,
        blank=True
    )

    updated_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-updated_at"]

        indexes = [
            models.Index(
                fields=["stock", "-updated_at"]
            ),
        ]

    def __str__(self):
        return f"{self.stock.symbol}: {self.current_price}"
```

### Why ForeignKey?

One stock can have many historical price records.

For example:

```text
AAPL
 |
 |--- 225.50
 |--- 226.10
 |--- 224.80
 |--- 227.20
```

The `ForeignKey` establishes a one-to-many relationship.

Each row represents a price snapshot, not necessarily every exchange trade.

## C. MarketNews Model

```python
class MarketNews(models.Model):

    external_id = models.CharField(
        max_length=255,
        unique=True
    )

    headline = models.CharField(
        max_length=500
    )

    summary = models.TextField(
        blank=True
    )

    source = models.CharField(
        max_length=150,
        blank=True
    )

    url = models.URLField(
        max_length=1000
    )

    image = models.URLField(
        max_length=1000,
        blank=True
    )

    category = models.CharField(
        max_length=100,
        blank=True
    )

    published_at = models.DateTimeField(
        null=True,
        blank=True
    )

    class Meta:
        ordering = ["-published_at"]

    def __str__(self):
        return self.headline
```

---

# 12. User Authentication

Django provides built-in authentication.

We will use:

- User model
- UserCreationForm
- LoginView
- LogoutView
- login_required
- IsAuthenticated

## accounts/forms.py

```python
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserRegistrationForm(UserCreationForm):

    email = forms.EmailField(
        required=True
    )

    class Meta:
        model = User

        fields = [
            "username",
            "email",
            "password1",
            "password2",
        ]

    def clean_email(self):
        email = self.cleaned_data["email"]

        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                "This email is already registered."
            )

        return email

    def save(self, commit=True):
        user = super().save(commit=False)

        user.email = self.cleaned_data["email"]

        if commit:
            user.save()

        return user
```

## accounts/views.py

```python
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import UserRegistrationForm


def register(request):

    if request.method == "POST":

        form = UserRegistrationForm(request.POST)

        if form.is_valid():

            user = form.save()

            login(request, user)

            return redirect("dashboard")

    else:

        form = UserRegistrationForm()

    return render(
        request,
        "register.html",
        {"form": form}
    )
```

## Authentication URLs

`accounts/urls.py`

```python
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from . import views

urlpatterns = [

    path(
        "register/",
        views.register,
        name="register"
    ),

    path(
        "login/",
        LoginView.as_view(
            template_name="login.html"
        ),
        name="login"
    ),

    path(
        "logout/",
        LogoutView.as_view(),
        name="logout"
    ),
]
```

Logout should be submitted through POST with CSRF protection.

---

# 13. Finnhub API Integration

The service layer handles external API communication.

It separates API logic from Django views and Celery tasks.

## apps/stocks/services.py

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
            raise FinnhubError(
                "Finnhub API key is missing."
            )

    def get(self, endpoint, params=None):

        request_params = dict(params or {})

        request_params["token"] = self.token

        try:

            response = httpx.get(
                f"{self.BASE_URL}/{endpoint}",
                params=request_params,
                timeout=15
            )

            if response.status_code == 429:
                raise FinnhubError(
                    "Finnhub API rate limit exceeded."
                )

            response.raise_for_status()

            data = response.json()

            if isinstance(data, dict) and data.get("error"):
                raise FinnhubError(data["error"])

            return data

        except httpx.HTTPStatusError as exc:

            raise FinnhubError(
                f"Finnhub HTTP error: {exc.response.status_code}"
            ) from exc

        except httpx.TimeoutException as exc:

            raise FinnhubError(
                "Finnhub API request timed out."
            ) from exc

        except httpx.RequestError as exc:

            raise FinnhubError(
                "Finnhub network connection error."
            ) from exc

        except ValueError as exc:

            raise FinnhubError(
                "Invalid JSON response."
            ) from exc

    def quote(self, symbol):

        symbol = symbol.strip().upper()

        data = self.get(
            "quote",
            {"symbol": symbol}
        )

        if not isinstance(data, dict):
            raise FinnhubError(
                "Invalid quote response."
            )

        if not data.get("c") or data["c"] <= 0:
            raise FinnhubError(
                f"No valid quote found for {symbol}."
            )

        return data

    def market_news(self, category="general"):

        return self.get(
            "news",
            {"category": category}
        )

    def candles(
        self,
        symbol,
        resolution,
        start,
        end
    ):

        data = self.get(
            "stock/candle",
            {
                "symbol": symbol,
                "resolution": resolution,
                "from": start,
                "to": end,
            }
        )

        if data.get("s") != "ok":
            raise FinnhubError(
                f"No historical data found for {symbol}."
            )

        return data

    def company_profile(self, symbol):

        return self.get(
            "stock/profile2",
            {"symbol": symbol}
        )
```

### Service Layer Benefits

1. Reusable API functions.
2. Easier error handling.
3. Cleaner views.
4. Easier unit testing.
5. Separation of business logic.

**Important:** Finnhub API limits depend on the account and subscription. Polling many symbols every 60 seconds may exceed the available quota. The actual schedule must be designed around the provider's current limits.

---

# 14. Stock Serializers

File: `apps/stocks/serializers.py`

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
            "market_timestamp",
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

### What is a Serializer?

A serializer converts complex Python objects, such as Django model instances, into JSON-compatible data.

It can also validate incoming data.

---

# 15. Stock REST API

File: `apps/stocks/views.py`

```python
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import Stock, MarketNews
from .serializers import StockSerializer, MarketNewsSerializer
from .services import FinnhubClient, FinnhubError


class StockListAPIView(generics.ListAPIView):

    queryset = Stock.objects.filter(
        is_active=True
    )

    serializer_class = StockSerializer

    permission_classes = [AllowAny]


class StockDetailAPIView(generics.RetrieveAPIView):

    queryset = Stock.objects.filter(
        is_active=True
    )

    serializer_class = StockSerializer

    lookup_field = "symbol"

    permission_classes = [AllowAny]


class NewsListAPIView(generics.ListAPIView):

    queryset = MarketNews.objects.all()

    serializer_class = MarketNewsSerializer

    permission_classes = [AllowAny]


class RefreshStockAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, symbol):

        try:

            stock = Stock.objects.get(
                symbol=symbol.upper(),
                is_active=True
            )

            quote = FinnhubClient().quote(
                stock.symbol
            )

            return Response({
                "symbol": stock.symbol,
                "quote": quote,
            })

        except Stock.DoesNotExist:

            return Response(
                {"error": "Stock not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        except FinnhubError as exc:

            return Response(
                {"error": str(exc)},
                status=status.HTTP_502_BAD_GATEWAY
            )
```

**Important:** This manual refresh example returns the quote but does not save it. The scheduled Celery task handles persistence. If manual refresh must update the database, reuse a shared quote-saving service rather than duplicating persistence logic.

---

# 16. Portfolio Management

A portfolio belongs to a user and can contain multiple stocks.

## apps/portfolio/models.py

```python
from django.conf import settings
from django.db import models

from apps.stocks.models import Stock


class Portfolio(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="portfolio"
    )

    stocks = models.ManyToManyField(
        Stock,
        blank=True,
        related_name="portfolios"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.user.username}'s Portfolio"
```

### Relationship

```text
User
 |
 | OneToOne
 |
Portfolio
 |
 | ManyToMany
 |
Stock
```

### Why ManyToManyField?

One portfolio can contain many stocks.

The same stock can belong to many users' portfolios.

## Portfolio API Logic

Every portfolio query must use the authenticated user.

Example:

```python
portfolio, created = Portfolio.objects.get_or_create(
    user=request.user
)
```

Never use an unrestricted portfolio query for private user data.

---

# 17. Watchlist Management

A watchlist allows a user to monitor stocks without necessarily treating them as owned portfolio assets.

## apps/watchlist/models.py

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

    created_at = models.DateTimeField(
        auto_now_add=True
    )

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

## Watchlist Serializer

`apps/watchlist/serializers.py`

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

        fields = [
            "id",
            "stock",
            "symbol",
            "name",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
        ]
```

## Watchlist Views

`apps/watchlist/views.py`

```python
from rest_framework import generics, serializers
from rest_framework.permissions import IsAuthenticated

from apps.stocks.models import Stock

from .models import WatchlistItem
from .serializers import WatchlistSerializer


class WatchlistListCreateAPIView(
    generics.ListCreateAPIView
):

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


class WatchlistDeleteAPIView(
    generics.DestroyAPIView
):

    serializer_class = WatchlistSerializer

    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        return WatchlistItem.objects.filter(
            user=self.request.user
        )
```

The unique database constraint protects against duplicate watchlist entries. The API should also handle duplicate-creation validation errors gracefully.

## Watchlist URLs

`apps/watchlist/urls.py`

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
        name="watchlist-list"
    ),

    path(
        "<int:pk>/",
        WatchlistDeleteAPIView.as_view(),
        name="watchlist-delete"
    ),
]
```

---

# 18. Historical Stock Data

Historical data is used to generate price charts.

Finnhub endpoint:

```text
GET /stock/candle
```

## Parameters

| Parameter | Meaning |
|---|---|
| symbol | Stock symbol |
| resolution | Candle interval |
| from | Start Unix timestamp |
| to | End Unix timestamp |
| token | API key |

## Response Fields

| Field | Meaning |
|---|---|
| c | Close price |
| h | High price |
| l | Low price |
| o | Open price |
| t | Timestamp |
| v | Volume |
| s | Response status |

## Example Python

```python
import time

from datetime import datetime, timezone

from apps.stocks.services import FinnhubClient


end = int(time.time())

start = end - (
    7 * 24 * 60 * 60
)

client = FinnhubClient()

data = client.candles(
    symbol="AAPL",
    resolution="D",
    start=start,
    end=end,
)

for timestamp, close in zip(
    data["t"],
    data["c"]
):

    date = datetime.fromtimestamp(
        timestamp,
        tz=timezone.utc
    )

    print(date, close)
```

## Common Resolutions

- 1
- 5
- 15
- 30
- 60
- D
- W
- M

Availability depends on Finnhub's supported endpoint rules and subscription.

Historical data should ideally be stored separately from frequent quote snapshots if the application needs efficient long-term chart queries.

---

# 19. Market News Integration

Finnhub provides market news.

Endpoint:

```text
GET /news?category=general
```

## News Synchronization Service

Create `apps/stocks/news_services.py` or keep this function in `services.py`.

```python
from datetime import datetime, timezone

from .models import MarketNews
from .services import FinnhubClient


def sync_market_news():

    client = FinnhubClient()

    articles = client.market_news("general")

    for article in articles:

        external_id = str(
            article.get("id") or article.get("url") or ""
        )

        if not external_id:
            continue

        published = article.get("datetime")

        published_at = (
            datetime.fromtimestamp(
                published,
                tz=timezone.utc
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

Use a Celery task to execute this function periodically.

---

# 20. Celery Configuration

Celery is used for background processing.

Examples:

- Fetch stock quotes.
- Synchronize market news.
- Check price alerts.
- Send notifications.
- Execute recurring jobs.

## config/celery.py

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

## config/__init__.py

```python
from .celery import app as celery_app

__all__ = ("celery_app",)
```

## Celery Settings

Add to `settings.py`:

```python
CELERY_BROKER_URL = REDIS_URL

CELERY_RESULT_BACKEND = REDIS_URL

CELERY_ACCEPT_CONTENT = ["json"]

CELERY_TASK_SERIALIZER = "json"

CELERY_RESULT_SERIALIZER = "json"

CELERY_TIMEZONE = "Asia/Dhaka"

CELERY_TASK_TRACK_STARTED = True

CELERY_TASK_TIME_LIMIT = 120
```

## Celery Beat Schedule

```python
CELERY_BEAT_SCHEDULE = {

    "refresh-stock-prices": {

        "task": "apps.stocks.tasks.refresh_stock_quotes",

        "schedule": STOCK_POLL_SECONDS,
    },

    "check-price-alerts": {

        "task": "apps.notifications.tasks.check_price_alerts",

        "schedule": 60.0,
    },

    "sync-market-news": {

        "task": "apps.stocks.tasks.sync_market_news_task",

        "schedule": 300.0,
    },

}
```

### Celery Worker vs Celery Beat

**Celery Worker:**
- Executes tasks.
- Performs background jobs.
- Processes queued messages.

**Celery Beat:**
- Schedules recurring tasks.
- Sends scheduled tasks to the broker.
- Does not itself execute the task logic.

Run only one Beat scheduler for a given schedule unless using an appropriate distributed scheduler/locking strategy.

---

# 21. Celery Background Tasks

File: `apps/stocks/tasks.py`

```python
from decimal import Decimal

from celery import shared_task

from asgiref.sync import async_to_sync

from channels.layers import get_channel_layer

from django.utils import timezone

from .models import Stock, StockPrice

from .services import FinnhubClient, FinnhubError


@shared_task
def refresh_stock_quotes():

    stocks = Stock.objects.filter(
        is_active=True
    )

    client = FinnhubClient()

    channel_layer = get_channel_layer()

    for stock in stocks:

        try:

            quote = client.quote(
                stock.symbol
            )

            price = StockPrice.objects.create(

                stock=stock,

                current_price=Decimal(
                    str(quote["c"])
                ),

                change=Decimal(
                    str(quote.get("d") or 0)
                ),

                percent_change=Decimal(
                    str(quote.get("dp") or 0)
                ),

                high_price=Decimal(
                    str(quote.get("h") or 0)
                ),

                low_price=Decimal(
                    str(quote.get("l") or 0)
                ),

                open_price=Decimal(
                    str(quote.get("o") or 0)
                ),

                previous_close=Decimal(
                    str(quote.get("pc") or 0)
                ),

                market_timestamp=(
                    timezone.datetime.fromtimestamp(
                        quote["t"],
                        tz=timezone.utc
                    )
                    if quote.get("t")
                    else None
                ),
            )

            payload = {

                "symbol": stock.symbol,

                "name": stock.name,

                "current_price": str(
                    price.current_price
                ),

                "change": str(
                    price.change
                ),

                "percent_change": str(
                    price.percent_change
                ),

                "updated_at": price.updated_at.isoformat(),
            }

            async_to_sync(
                channel_layer.group_send
            )(
                "stock_updates",
                {
                    "type": "stock.price",
                    "data": payload,
                }
            )

        except FinnhubError as exc:

            print(
                f"Finnhub error for {stock.symbol}: {exc}"
            )

        except Exception as exc:

            print(
                f"Unexpected error for {stock.symbol}: {exc}"
            )


@shared_task
def sync_market_news_task():

    from .news_services import sync_market_news

    sync_market_news()
```

**Implementation note:** Import `timezone` from `datetime` for the timestamp conversion:

```python
from datetime import timezone
```

The production implementation should use structured logging rather than `print()`, and should carefully handle API failures, retries, rate limits, and task concurrency.

## Why async_to_sync()?

Celery tasks are synchronous in this implementation, while Channels' channel layer methods are asynchronous.

`async_to_sync()` allows a synchronous task to call an asynchronous function.

---

# 22. Redis Configuration

Redis is an in-memory data store.

In this project, Redis serves as:

1. Celery message broker.
2. Optional Celery result backend.
3. Django Channels channel layer.

## Run Redis with Docker

```bash
docker run --name stock-redis -p 6379:6379 -d redis:7
```

Check Redis:

```bash
docker exec -it stock-redis redis-cli ping
```

Expected response:

```text
PONG
```

## Redis Connection URL

```env
REDIS_URL=redis://127.0.0.1:6379/0
```

Redis should not be exposed publicly without proper authentication and network security.

---

# 23. Django Channels Configuration

Django Channels extends Django to support protocols such as WebSocket.

## apps/stocks/consumers.py

```python
import json

from channels.generic.websocket import AsyncWebsocketConsumer


class StockConsumer(AsyncWebsocketConsumer):

    async def connect(self):

        if not self.scope["user"].is_authenticated:

            await self.close(code=4401)

            return

        self.group_name = "stock_updates"

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):

        if hasattr(self, "group_name"):

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

### Consumer Responsibilities

- Accept WebSocket connections.
- Reject unauthenticated connections.
- Join a Channels group.
- Receive group events.
- Send stock updates to connected browsers.
- Leave the group on disconnect.

**Security note:** This example uses session authentication and a global group for public market data. For private portfolio information, create user-specific groups and verify that each user can only join their own authorized group.

## apps/stocks/routing.py

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

## config/asgi.py

```python
import os

from django.core.asgi import get_asgi_application

from channels.routing import ProtocolTypeRouter, URLRouter

from channels.auth import AuthMiddlewareStack

from channels.security.websocket import (
    AllowedHostsOriginValidator
)


os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "config.settings"
)

django_asgi_app = get_asgi_application()

from apps.stocks.routing import websocket_urlpatterns


application = ProtocolTypeRouter({

    "http": django_asgi_app,

    "websocket": AllowedHostsOriginValidator(

        AuthMiddlewareStack(

            URLRouter(
                websocket_urlpatterns
            )

        )

    ),

})
```

For production, configure allowed hosts carefully. For cross-domain deployments, configure explicit trusted origins and authentication rules.

---

# 24. Price Alert System

Users can create price alerts.

Examples:

- Notify when AAPL goes above $250.
- Notify when TSLA goes below $300.

## apps/notifications/models.py

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
        on_delete=models.CASCADE,
        related_name="price_alerts"
    )

    stock = models.ForeignKey(
        Stock,
        on_delete=models.CASCADE
    )

    target_price = models.DecimalField(
        max_digits=18,
        decimal_places=4
    )

    condition = models.CharField(
        max_length=10,
        choices=CONDITION_CHOICES
    )

    is_triggered = models.BooleanField(
        default=False
    )

    triggered_at = models.DateTimeField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return (
            f"{self.stock.symbol} "
            f"{self.condition} "
            f"{self.target_price}"
        )
```

## Price Alert Logic

File: `apps/notifications/tasks.py`

```python
from celery import shared_task

from django.db import transaction
from django.utils import timezone

from .models import PriceAlert

from apps.stocks.models import StockPrice


@shared_task
def check_price_alerts():

    alerts = PriceAlert.objects.filter(
        is_triggered=False
    ).select_related("stock", "user")

    for alert in alerts:

        latest_price = StockPrice.objects.filter(
            stock=alert.stock
        ).first()

        if not latest_price:
            continue

        current = latest_price.current_price

        target = alert.target_price

        triggered = (

            alert.condition == "above"
            and current >= target

        ) or (

            alert.condition == "below"
            and current <= target

        )

        if triggered:

            with transaction.atomic():

                updated = PriceAlert.objects.filter(
                    pk=alert.pk,
                    is_triggered=False
                ).update(
                    is_triggered=True,
                    triggered_at=timezone.now()
                )

            if updated:

                # Add notification delivery here.
                # Example: enqueue an email task.

                pass
```

The conditional database update helps prevent multiple workers from triggering the same alert simultaneously.

## Notification Types

- In-app notification
- Email notification
- Browser notification

Email delivery should run as a separate Celery task.

---

# 25. Stock Seeding

Create the following folders:

```text
apps/stocks/management/
    __init__.py
    commands/
        __init__.py
        seed_stocks.py
```

## seed_stocks.py

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

                defaults={
                    "name": name,
                    "is_active": True,
                }

            )

        self.stdout.write(
            self.style.SUCCESS(
                "Stocks seeded successfully."
            )
        )
```

Run:

```bash
python manage.py seed_stocks
```

The seed command creates initial stock records. It does not fetch their prices.

---

# 26. Frontend Dashboard

The dashboard uses:

- HTML
- Bootstrap 5
- JavaScript
- Fetch API
- WebSocket
- Chart.js

## templates/base.html

```html
<!DOCTYPE html>
<html lang="en">

<head>

    <meta charset="UTF-8">

    <meta name="viewport"
          content="width=device-width, initial-scale=1">

    <title>{% block title %}Stock Tracker{% endblock %}</title>

    <link
        href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css"
        rel="stylesheet"
    >

</head>

<body class="bg-light">

    <nav class="navbar navbar-dark bg-dark">

        <div class="container">

            <a class="navbar-brand" href="/">
                Stock Tracker
            </a>

            {% if user.is_authenticated %}

                <form method="post" action="{% url 'logout' %}">
                    {% csrf_token %}
                    <button class="btn btn-outline-light btn-sm">
                        Logout
                    </button>
                </form>

            {% endif %}

        </div>

    </nav>

    <main class="container py-4">

        {% block content %}
        {% endblock %}

    </main>

    {% block scripts %}
    {% endblock %}

</body>

</html>
```

## templates/dashboard.html

```html
{% extends "base.html" %}

{% load static %}

{% block title %}
Realtime Stock Tracker
{% endblock %}

{% block content %}

<h2 class="mb-4">
    Realtime Stock Dashboard
</h2>

<div class="mb-3">

    WebSocket Status:

    <span
        id="connection-status"
        class="badge text-bg-secondary"
    >
        Connecting...
    </span>

</div>

<div class="card shadow-sm">

    <div class="card-body">

        <h5 class="mb-3">
            Stock Market
        </h5>

        <div class="table-responsive">

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
                        <td colspan="5">
                            Loading stocks...
                        </td>
                    </tr>

                </tbody>

            </table>

        </div>

    </div>

</div>

{% endblock %}

{% block scripts %}

<script src="{% static 'js/dashboard.js' %}"></script>

{% endblock %}
```

## Dashboard View

Add to `apps/stocks/views.py`:

```python
from django.contrib.auth.decorators import login_required

from django.shortcuts import render


@login_required
def dashboard(request):

    return render(
        request,
        "dashboard.html"
    )
```

---

# 27. JavaScript WebSocket Client

File: `static/js/dashboard.js`

```javascript
const tableBody = document.getElementById(
    "stock-table-body"
);

const statusElement = document.getElementById(
    "connection-status"
);

const rows = new Map();


function createCell(value) {

    const td = document.createElement("td");

    td.textContent = value ?? "-";

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

        createCell(
            `${stock.percent_change}%`
        ),

        createCell(stock.updated_at)

    );

}


async function loadStocks() {

    const response = await fetch(
        "/api/stocks/"
    );

    if (!response.ok) {

        throw new Error(
            "Unable to load stocks."
        );

    }

    const stocks = await response.json();

    rows.clear();

    tableBody.replaceChildren();

    stocks.forEach(stock => {

        const latest = stock.latest_price;

        if (!latest) return;

        renderStock({

            symbol: stock.symbol,

            name: stock.name,

            current_price: latest.current_price,

            percent_change: latest.percent_change,

            updated_at: latest.updated_at,

        });

    });

}


let socket = null;

let reconnectTimer = null;


function updateStatus(text, className) {

    statusElement.textContent = text;

    statusElement.className = className;

}


function connectWebSocket() {

    if (
        socket &&
        (
            socket.readyState === WebSocket.OPEN ||
            socket.readyState === WebSocket.CONNECTING
        )
    ) {
        return;
    }

    const protocol = (
        location.protocol === "https:"
    ) ? "wss:" : "ws:";

    socket = new WebSocket(
        `${protocol}//${location.host}/ws/stocks/`
    );


    socket.onopen = () => {

        updateStatus(
            "Connected",
            "badge text-bg-success"
        );

    };


    socket.onmessage = event => {

        try {

            const message = JSON.parse(event.data);

            if (
                message.type === "stock_update"
            ) {

                renderStock(message.data);

            }

        } catch (error) {

            console.error(
                "Invalid WebSocket message:",
                error
            );

        }

    };


    socket.onclose = () => {

        updateStatus(
            "Disconnected",
            "badge text-bg-danger"
        );

        reconnectTimer = setTimeout(
            connectWebSocket,
            3000
        );

    };


    socket.onerror = error => {

        console.error(
            "WebSocket error:",
            error
        );

        socket.close();

    };

}


loadStocks().catch(error => {

    console.error(error);

});

connectWebSocket();
```

### Important JavaScript Concepts

**Fetch API:**

Used to retrieve stock data from Django REST APIs.

**WebSocket:**

Used to receive updates from the server without repeatedly sending HTTP requests.

**DOM Manipulation:**

Used to update stock rows dynamically.

**Map:**

Used to keep track of existing stock table rows.

**textContent:**

Used instead of unsafe HTML insertion to reduce XSS risks.

**Reconnection:**

Attempts to reconnect after the WebSocket connection closes.

For a production client, add exponential backoff, connection cleanup, and duplicate timer prevention.

---

# 28. Chart.js Historical Price Chart

Include Chart.js:

```html
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
```

Example HTML:

```html
<canvas id="stock-chart"></canvas>
```

Example JavaScript:

```javascript
const chartContext = document
    .getElementById("stock-chart")
    .getContext("2d");


const stockChart = new Chart(
    chartContext,
    {
        type: "line",

        data: {
            labels: [],

            datasets: [
                {
                    label: "Stock Price",

                    data: [],

                    tension: 0.3
                }
            ]
        },

        options: {
            responsive: true,

            maintainAspectRatio: false,

            scales: {
                y: {
                    beginAtZero: false
                }
            }
        }
    }
);


function updateChart(labels, prices) {

    stockChart.data.labels = labels;

    stockChart.data.datasets[0].data = prices;

    stockChart.update();

}
```

The historical API endpoint should return properly formatted dates and prices before calling `updateChart()`.

---

# 29. URL Configuration

## apps/stocks/urls.py

```python
from django.urls import path

from .views import (
    StockListAPIView,
    StockDetailAPIView,
    NewsListAPIView,
    RefreshStockAPIView,
    dashboard,
)


urlpatterns = [

    path(
        "",
        StockListAPIView.as_view(),
        name="stock-list"
    ),

    path(
        "news/",
        NewsListAPIView.as_view(),
        name="news-list"
    ),

    path(
        "<str:symbol>/refresh/",
        RefreshStockAPIView.as_view(),
        name="stock-refresh"
    ),

    path(
        "<str:symbol>/",
        StockDetailAPIView.as_view(),
        name="stock-detail"
    ),

]
```

## config/urls.py

```python
from django.contrib import admin

from django.urls import path, include

from apps.stocks.views import dashboard


urlpatterns = [

    path(
        "admin/",
        admin.site.urls
    ),

    path(
        "",
        dashboard,
        name="dashboard"
    ),

    path(
        "accounts/",
        include("apps.accounts.urls")
    ),

    path(
        "api/stocks/",
        include("apps.stocks.urls")
    ),

    path(
        "api/watchlist/",
        include("apps.watchlist.urls")
    ),

]
```

**Important:** The `news/` route is placed before the dynamic `<str:symbol>/` route so that the URL router resolves it correctly.

The accounts URLs are prefixed with `/accounts/`, so the login and logout URLs become `/accounts/login/` and `/accounts/logout/`. Keep the settings redirects consistent with these paths, or configure the account URLs at the root instead.

---

# 30. API Endpoints

| Method | Endpoint | Purpose | Access |
|---|---|---|---|
| GET | `/` | Dashboard | Authenticated |
| GET | `/accounts/login/` | Login page | Public |
| POST | `/accounts/login/` | Login | Public |
| GET/POST | `/accounts/register/` | Registration | Public |
| POST | `/accounts/logout/` | Logout | Authenticated |
| GET | `/api/stocks/` | List stocks | Public |
| GET | `/api/stocks/AAPL/` | Stock details | Public |
| POST | `/api/stocks/AAPL/refresh/` | Manual refresh | Authenticated |
| GET | `/api/stocks/news/` | Market news | Public |
| GET | `/api/watchlist/` | User watchlist | Authenticated |
| POST | `/api/watchlist/` | Add watchlist item | Authenticated |
| DELETE | `/api/watchlist/1/` | Delete watchlist item | Authenticated |

WebSocket:

```text
ws://127.0.0.1:8000/ws/stocks/
```

Production:

```text
wss://your-domain.com/ws/stocks/
```

---

# 31. HTTP Status Codes

| Status | Meaning |
|---|---|
| 200 | OK |
| 201 | Created |
| 204 | No Content |
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 409 | Conflict |
| 429 | Too Many Requests |
| 500 | Internal Server Error |
| 502 | Bad Gateway |
| 503 | Service Unavailable |

### Important Differences

**400 Bad Request:**

Invalid request data.

**401 Unauthorized:**

Authentication is missing or invalid.

**403 Forbidden:**

The user is not allowed to perform the operation.

**404 Not Found:**

The requested resource does not exist or is not accessible.

**409 Conflict:**

A request conflicts with existing data, such as a duplicate item.

**429 Too Many Requests:**

Rate limit exceeded.

**502 Bad Gateway:**

An upstream service, such as Finnhub, returned an error.

---

# 32. Security Implementation

## A. Authentication

Django:

```python
@login_required
```

DRF:

```python
permission_classes = [IsAuthenticated]
```

## B. CSRF Protection

HTML forms:

```html
<form method="post">

    {% csrf_token %}

    <button type="submit">
        Submit
    </button>

</form>
```

JavaScript POST requests using session authentication should include the CSRF token.

## C. Environment Variables

```python
FINNHUB_API_KEY = os.getenv(
    "FINNHUB_API_KEY"
)
```

Never store API keys in frontend code or public repositories.

## D. User-Specific Data

```python
Portfolio.objects.get_or_create(
    user=request.user
)
```

Watchlist:

```python
WatchlistItem.objects.filter(
    user=request.user
)
```

Always filter private records by the authenticated user.

## E. Rate Limiting

Rate limiting can protect expensive endpoints.

Example:

```python
from django_ratelimit.decorators import ratelimit


@ratelimit(
    key="user_or_ip",
    rate="60/m",
    block=True
)
def example_view(request):
    pass
```

For DRF endpoints, use an appropriate DRF throttling class or custom throttling implementation.

## F. WebSocket Security

- Require authentication.
- Validate the connection origin.
- Protect private channel groups.
- Avoid trusting client-supplied user IDs.
- Validate incoming messages.
- Use WSS in production.

## G. XSS Prevention

Avoid:

```javascript
element.innerHTML = userInput;
```

Prefer:

```javascript
element.textContent = userInput;
```

## H. Database Integrity

Use database constraints for:

- Unique stock symbols.
- Unique user-stock watchlist pairs.
- Valid foreign-key relationships.

---

# 33. Error Handling

## Finnhub Errors

Possible errors:

- Missing API key.
- Invalid API key.
- API access denied.
- Rate limit exceeded.
- Network error.
- Request timeout.
- Invalid JSON.
- No stock data available.

## Django Errors

- ValidationError
- DoesNotExist
- IntegrityError
- PermissionDenied
- Http404

## Celery Errors

- Redis connection failure.
- Task timeout.
- External API failure.
- Duplicate scheduled task.
- Database failure.

Production applications should use structured logging, error monitoring, retry policies, and appropriate user-facing error messages.

Never expose secret keys, database credentials, or internal exception tracebacks to API clients.

---

# 34. Database Migrations

Create migrations:

```bash
python manage.py makemigrations
```

Apply migrations:

```bash
python manage.py migrate
```

Check migrations:

```bash
python manage.py showmigrations
```

Create superuser:

```bash
python manage.py createsuperuser
```

Run system checks:

```bash
python manage.py check
```

---

# 35. Running the Complete Project

Several services must run simultaneously.

## Terminal 1: Redis

```bash
docker start stock-redis
```

## Terminal 2: Django ASGI Server

```bash
python manage.py runserver
```

For local development, Daphne can also be used explicitly:

```bash
daphne -p 8000 config.asgi:application
```

## Terminal 3: Celery Worker

Windows:

```powershell
celery -A config worker -l info -P solo
```

Linux/macOS:

```bash
celery -A config worker -l info
```

## Terminal 4: Celery Beat

```bash
celery -A config beat -l info
```

### Important

- Redis must be running.
- Django must be configured with ASGI.
- Celery Worker must be running.
- Celery Beat must be running.
- Finnhub API key must be valid.
- Database migrations must be applied.

---

# 36. Testing Strategy

Testing should cover models, APIs, services, authentication, background tasks, and WebSocket communication.

## A. Model Testing

- Stock can be created.
- Stock symbol is unique.
- Portfolio belongs to one user.
- Watchlist prevents duplicates.
- PriceAlert saves correctly.

## B. API Testing

- Stock list returns JSON.
- Stock detail returns the correct stock.
- News endpoint returns articles.
- Unauthenticated users cannot access private APIs.
- A user cannot delete another user's watchlist item.

## C. Service Testing

Mock Finnhub responses to test:

- Successful quote.
- Invalid API key.
- Rate limit.
- Timeout.
- Invalid response.
- Missing stock data.

## D. Celery Testing

- Stock task executes.
- Price snapshots are saved.
- API errors are handled.
- Alert task triggers correctly.
- News sync saves articles.

## E. WebSocket Testing

Use Django Channels testing utilities:

```python
from channels.testing import WebsocketCommunicator
```

Test:

- Authenticated connection succeeds.
- Unauthenticated connection is rejected.
- Group messages are received.
- Disconnect removes the channel from its group.

## F. Frontend Testing

- Dashboard loads.
- Stock rows appear.
- WebSocket connects.
- Prices update.
- Connection status changes.
- Reconnection works.
- Browser console has no unexpected errors.

---

# 37. Common Problems and Solutions

## Problem 1: Redis Connection Refused

Cause:
- Redis is not running.
- Redis URL is incorrect.

Solution:

```bash
docker start stock-redis
```

Check:

```bash
docker exec -it stock-redis redis-cli ping
```

## Problem 2: Finnhub API Key Missing

Check:

```env
FINNHUB_API_KEY=your_api_key
```

Verify:

- `.env` exists.
- `load_dotenv()` is configured.
- The key is correct.
- Django and Celery processes have loaded the environment.

Restart processes after changing environment variables.

## Problem 3: WebSocket 404

Check:

- `ASGI_APPLICATION`
- `config/asgi.py`
- `apps/stocks/routing.py`
- WebSocket URL
- ASGI server

## Problem 4: WebSocket 403

Possible reasons:

- Origin validation failed.
- Authentication is missing.
- User is not logged in.
- Cookie/session was not sent.

## Problem 5: Celery Task Not Running

Check:

- Redis connection.
- Celery worker.
- Celery Beat.
- Task import path.
- `autodiscover_tasks()`.
- Task name in Beat schedule.

## Problem 6: Stock Price Not Updating

Check:

- Finnhub token.
- API quota.
- Celery worker logs.
- Stock active status.
- Celery Beat schedule.
- Database records.

## Problem 7: Duplicate Watchlist Item

Cause:

The user attempts to add the same stock twice.

Solution:

Use a database `UniqueConstraint` and return a clear validation response.

## Problem 8: WebSocket Connects but Receives No Updates

Check:

- Celery task executes.
- `group_send()` is called.
- Consumer event handler is named correctly.
- Redis channel layer works.
- Frontend message handler works.

## Problem 9: API Returns 401 or 403

Check:

- Session authentication.
- Login status.
- DRF permission classes.
- CSRF token for session-authenticated POST requests.

---

# 38. Performance Optimization

## Database

- Use indexes.
- Use `select_related()`.
- Use `prefetch_related()`.
- Paginate large API responses.
- Avoid unnecessary database queries.

Example:

```python
WatchlistItem.objects.filter(
    user=request.user
).select_related("stock")
```

## Redis

Use Redis for:

- Temporary caching.
- Message brokering.
- Channel layers.

## Celery

- Limit task concurrency appropriately.
- Add retries with exponential backoff.
- Prevent overlapping scheduled tasks.
- Monitor task failures.
- Avoid excessive API calls.

## Finnhub

- Respect provider rate limits.
- Cache data where appropriate.
- Avoid repeated requests for identical data.
- Poll only the symbols that need updates.
- Consider batch scheduling and API quotas.

## WebSocket

- Avoid unnecessary broadcasts.
- Use private groups where necessary.
- Send compact JSON messages.
- Disconnect inactive clients.

## Stock Price Storage

Saving every polling result indefinitely can grow the database quickly.

Possible improvements:

- Retain recent quote snapshots.
- Archive old snapshots.
- Use a separate historical candle table.
- Add periodic cleanup tasks.

---

# 39. Production Deployment

Before deploying:

1. Set `DEBUG=False`.
2. Use a strong secret key.
3. Configure PostgreSQL.
4. Configure Redis securely.
5. Configure HTTPS and WSS.
6. Configure trusted hosts and WebSocket origins.
7. Protect API credentials.
8. Configure logging.
9. Configure database backups.
10. Add automated tests.
11. Configure static file serving.
12. Monitor Celery workers.
13. Monitor Celery Beat.
14. Configure API rate limits.
15. Add health checks.

## Recommended Production Services

| Service | Responsibility |
|---|---|
| Nginx | Reverse proxy |
| Daphne or Uvicorn | ASGI application server |
| PostgreSQL | Main database |
| Redis | Broker and channel layer |
| Celery Worker | Background tasks |
| Celery Beat | Scheduled tasks |
| HTTPS Certificate | Secure connections |

A production deployment should separate web serving, background workers, scheduling, and infrastructure configuration.

---

# 40. Git and GitHub

Initialize repository:

```bash
git init
```

Add files:

```bash
git add .
```

Commit:

```bash
git commit -m "Initial realtime stock tracker project"
```

Create a GitHub repository and connect it:

```bash
git remote add origin YOUR_GITHUB_REPOSITORY_URL
```

Push:

```bash
git branch -M main
git push -u origin main
```

Never commit:

- `.env`
- API tokens
- Database passwords
- Secret keys
- Private production credentials

---

# 41. Development Roadmap

## Phase 1: Django Fundamentals

Learn:

- Django project setup.
- Apps.
- Models.
- Views.
- URLs.
- Templates.
- ORM.
- Authentication.

Build:
- Basic Stock Tracker.
- Registration and Login.
- Portfolio CRUD.

## Phase 2: Finnhub Integration

Learn:

- HTTP requests.
- JSON parsing.
- API authentication.
- Error handling.
- API rate limits.
- Service layer.

Build:
- Current stock quote.
- Stock details.
- Market news.

## Phase 3: Django REST Framework

Learn:

- Serializers.
- APIView.
- GenericAPIView.
- ModelSerializer.
- Permissions.
- Authentication.
- Pagination.
- Throttling.

Build:
- Stock APIs.
- Portfolio APIs.
- Watchlist APIs.

## Phase 4: Database Design

Learn:

- ForeignKey.
- OneToOneField.
- ManyToManyField.
- UniqueConstraint.
- Database indexes.
- Query optimization.

Build:
- StockPrice history.
- Portfolio.
- Watchlist.
- PriceAlert.

## Phase 5: Redis and Celery

Learn:

- Redis.
- Message brokers.
- Celery tasks.
- Celery workers.
- Celery Beat.
- Retries.
- Task monitoring.

Build:
- Background stock updates.
- News synchronization.
- Price alert checks.

## Phase 6: Django Channels

Learn:

- ASGI.
- WebSocket.
- Consumers.
- Routing.
- Channel layers.
- Group broadcasting.
- WebSocket authentication.

Build:
- Realtime dashboard.
- Automatic price updates.

## Phase 7: Frontend

Learn:

- Bootstrap.
- JavaScript.
- Fetch API.
- DOM manipulation.
- WebSocket client.
- Chart.js.

Build:
- Responsive dashboard.
- Historical chart.
- Watchlist interface.
- Alert interface.

## Phase 8: Production

Learn:

- PostgreSQL.
- Docker.
- Nginx.
- Daphne.
- Deployment.
- Logging.
- Monitoring.
- Security.

Build:
- Production-ready deployment.

---

# 42. Interview Questions and Answers

## Django Questions

### Q1. What is Django?

Django is a high-level Python web framework used to build secure and maintainable web applications.

### Q2. What is Django ORM?

Django ORM allows developers to interact with relational databases using Python objects instead of writing SQL manually.

### Q3. What is ForeignKey?

ForeignKey creates a many-to-one relationship between two models.

### Q4. What is OneToOneField?

OneToOneField creates a one-to-one relationship between two models.

### Q5. What is ManyToManyField?

ManyToManyField creates a many-to-many relationship between two models.

### Q6. What is get_or_create()?

It retrieves an existing object or creates a new one if it does not exist.

### Q7. What is select_related()?

It uses SQL joins to retrieve related objects efficiently for ForeignKey and OneToOneField relationships.

### Q8. What is prefetch_related()?

It retrieves related objects using additional queries and joins the results in Python. It is useful for ManyToMany and reverse relationships.

## DRF Questions

### Q9. What is Django REST Framework?

DRF is a Django toolkit for building RESTful APIs.

### Q10. What is a serializer?

A serializer converts model instances into JSON-compatible data and validates incoming data.

### Q11. What is APIView?

APIView is a DRF class that provides methods for handling HTTP requests.

### Q12. What is the difference between APIView and GenericAPIView?

APIView provides basic API request handling. GenericAPIView adds common functionality such as queryset, serializer, and lookup configuration.

### Q13. What is IsAuthenticated?

It is a DRF permission class that allows access only to authenticated users.

## API Questions

### Q14. What is an API?

An API is an interface that allows different software systems to communicate.

### Q15. What is JSON?

JSON is a lightweight data interchange format.

### Q16. What is the difference between GET and POST?

GET retrieves information. POST submits data or requests creation of a resource.

### Q17. What is HTTP status code 400?

It indicates that the request contains invalid or unacceptable data.

### Q18. What is rate limiting?

Rate limiting restricts the number of requests allowed within a specified period.

## Celery Questions

### Q19. What is Celery?

Celery is a distributed task queue used for background processing.

### Q20. What is Redis?

Redis is an in-memory data store that can be used as a message broker, cache, and channel layer backend.

### Q21. What is Celery Beat?

Celery Beat schedules recurring tasks.

### Q22. What is the difference between Celery Worker and Celery Beat?

Worker executes tasks. Beat schedules and sends recurring tasks to the broker.

### Q23. Why use Celery in this project?

Celery retrieves stock prices and synchronizes news in the background without blocking normal web requests.

## WebSocket Questions

### Q24. What is WebSocket?

WebSocket is a communication protocol that provides persistent, bidirectional communication between a client and server.

### Q25. What is Django Channels?

Django Channels extends Django to support asynchronous protocols such as WebSocket.

### Q26. What is ASGI?

ASGI stands for Asynchronous Server Gateway Interface. It supports asynchronous Python web applications.

### Q27. What is the difference between HTTP and WebSocket?

HTTP typically follows a request-response model. WebSocket maintains a persistent connection that allows both sides to send messages.

### Q28. What is a Channels Group?

A Channels group allows multiple connected channel instances to receive broadcast events.

## Redis Questions

### Q29. Why is Redis used in this project?

Redis provides message transport for Celery and Channels and can also be used for caching.

### Q30. Is Redis the main database?

No. PostgreSQL is the main persistent database in production. Redis is used for messaging and temporary data.

## Project-Specific Questions

### Q31. How does stock price updating work?

Celery Beat schedules a task. A Celery Worker fetches stock quotes from Finnhub and saves them to PostgreSQL.

### Q32. How does the frontend receive updated prices?

The backend sends events through the Redis channel layer. Django Channels forwards them through WebSocket to the browser.

### Q33. Is this tick-by-tick realtime?

No. The basic implementation periodically fetches quotes through Finnhub REST API. It provides near-real-time polling updates.

### Q34. Why use a service layer?

It separates external API and business logic from views, making the code reusable and easier to maintain.

### Q35. How do you protect the Finnhub API key?

By storing it in environment variables and accessing it only from the backend.

### Q36. How do you prevent duplicate watchlist entries?

By using a database UniqueConstraint on the user and stock fields.

### Q37. How do you protect private user data?

By using authentication, permission classes, and user-filtered querysets.

### Q38. How do you prevent duplicate price alerts?

By using a conditional database update that only triggers an alert if it has not already been triggered.

### Q39. How do you handle Finnhub rate limits?

By respecting provider quotas, reducing unnecessary polling, caching responses, and applying retries with backoff where appropriate.

### Q40. Why use PostgreSQL?

PostgreSQL provides reliable relational data storage, indexing, transactions, and strong database integrity features.

---

# 43. Important Backend Concepts

## HTTP vs WebSocket

| HTTP | WebSocket |
|---|---|
| Request-response | Persistent connection |
| Client initiates requests | Both sides can send messages |
| Suitable for REST APIs | Suitable for realtime updates |
| Stateless at protocol level | Maintains a connection |

## Celery vs Django Channels

| Celery | Django Channels |
|---|---|
| Background tasks | Realtime communication |
| Scheduled jobs | WebSocket |
| External API polling | Browser updates |
| Email processing | Event broadcasting |

## Celery Worker vs Celery Beat

| Worker | Beat |
|---|---|
| Executes tasks | Schedules tasks |
| Processes queued jobs | Publishes scheduled jobs |
| Performs background work | Manages recurring execution |

## PostgreSQL vs Redis

| PostgreSQL | Redis |
|---|---|
| Persistent relational database | In-memory data store |
| Stores application records | Stores messages and temporary data |
| SQL queries | Key-value and data structure operations |
| Main database | Broker/cache/channel layer |

## Portfolio vs Watchlist

**Portfolio:**
- Represents stocks a user tracks as part of their portfolio.
- Can later support quantity, purchase price, and profit/loss.

**Watchlist:**
- Represents stocks a user wants to monitor.
- Does not necessarily mean the user owns those stocks.

---

# 44. Final Project Checklist

## Project Setup

- [ ] Create Django project.
- [ ] Create virtual environment.
- [ ] Install dependencies.
- [ ] Configure environment variables.
- [ ] Configure database.
- [ ] Configure Redis.

## Authentication

- [ ] Registration.
- [ ] Login.
- [ ] Logout.
- [ ] Password validation.
- [ ] Authentication permissions.

## Stock Management

- [ ] Stock model.
- [ ] StockPrice model.
- [ ] Finnhub service.
- [ ] Stock list API.
- [ ] Stock detail API.
- [ ] Manual price refresh.
- [ ] Historical price storage.

## Portfolio

- [ ] Portfolio model.
- [ ] Add stock.
- [ ] Remove stock.
- [ ] User-specific portfolio API.

## Watchlist

- [ ] Watchlist model.
- [ ] Add watchlist item.
- [ ] Delete watchlist item.
- [ ] Duplicate prevention.
- [ ] User-specific access.

## Market Data

- [ ] Finnhub quote integration.
- [ ] Company profile integration.
- [ ] Market news integration.
- [ ] Historical candle integration.

## Background Processing

- [ ] Celery configuration.
- [ ] Redis broker.
- [ ] Celery worker.
- [ ] Celery Beat.
- [ ] Price update task.
- [ ] News sync task.
- [ ] Price alert task.

## Realtime

- [ ] ASGI configuration.
- [ ] Channels configuration.
- [ ] Redis channel layer.
- [ ] WebSocket consumer.
- [ ] WebSocket routing.
- [ ] Browser connection.
- [ ] Automatic reconnection.
- [ ] Realtime price updates.

## Frontend

- [ ] Bootstrap dashboard.
- [ ] Stock table.
- [ ] WebSocket status.
- [ ] Historical chart.
- [ ] Watchlist interface.
- [ ] Price alert interface.
- [ ] Error messages.

## Security

- [ ] API key protection.
- [ ] CSRF protection.
- [ ] Authentication.
- [ ] Authorization.
- [ ] Rate limiting.
- [ ] Input validation.
- [ ] WebSocket origin validation.
- [ ] User-specific queries.

## Production

- [ ] PostgreSQL.
- [ ] DEBUG=False.
- [ ] HTTPS/WSS.
- [ ] Logging.
- [ ] Monitoring.
- [ ] Automated tests.
- [ ] Backups.
- [ ] Deployment.

---

# 45. Official Documentation

## Python and Django

- Python: https://docs.python.org/3/
- Django: https://docs.djangoproject.com/

## Django REST Framework

- https://www.django-rest-framework.org/

## Django Channels

- https://channels.readthedocs.io/

## Celery

- https://docs.celeryq.dev/

## Redis

- https://redis.io/docs/

## Finnhub

- https://finnhub.io/docs/api

## Bootstrap

- https://getbootstrap.com/docs/

## Chart.js

- https://www.chartjs.org/docs/

## PostgreSQL

- https://www.postgresql.org/docs/

## HTTPX

- https://www.python-httpx.org/

---

# 46. Final Project Summary

The Realtime Stock Tracker combines several important backend technologies into one practical application.

### What This Project Demonstrates

1. Django application architecture.
2. Database modeling and ORM.
3. User authentication and authorization.
4. REST API development.
5. External API integration.
6. API error handling.
7. Background task processing.
8. Scheduled task execution.
9. Redis message brokering.
10. WebSocket communication.
11. Realtime browser updates.
12. Historical data management.
13. User-specific portfolio and watchlist.
14. Price alert processing.
15. Security and production considerations.

### Project Classification

**Level:** Intermediate to Advanced

**Suitable for:**
- Python Backend Developer Portfolio
- Django Developer Portfolio
- Junior Backend Engineer Interviews
- Practical REST API Learning
- Asynchronous Programming Practice
- Realtime Application Development

### Important Final Note

This README is the complete project design and implementation guide. Not every feature is fully implemented in the code examples above. In particular, portfolio CRUD APIs, historical chart APIs, price-alert CRUD and notification delivery, automated tests, production monitoring, and deployment must be completed and tested separately.

The project should be developed in phases rather than implementing all technologies simultaneously.

**Recommended development order:**

Django Basics → Authentication → Database Models → Finnhub API → DRF → Portfolio → Watchlist → Celery → Redis → Channels → WebSocket → Historical Charts → Price Alerts → Testing → Deployment.

The goal is not simply to make the application work. The goal is to understand why each technology is used, how the components communicate, and how to build a maintainable backend system.
