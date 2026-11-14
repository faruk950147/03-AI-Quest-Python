# Django Stock Tracker – Complete Project Notes

## 1. Project Overview

**Project Name:** Stock Tracker  
**Framework:** Django  
**Programming Language:** Python  
**Frontend:** HTML, CSS, JavaScript  
**API Provider:** Finnhub API  
**Database:** SQLite / PostgreSQL  
**HTTP Client:** Requests  

### Main Features

- User Registration
- User Login and Logout
- Add Stock to Portfolio
- Delete Stock from Portfolio
- Fetch Real-Time Stock Quotes
- Update Stock Prices
- User-Specific Portfolio
- AJAX-Based Dashboard
- CSRF Protection
- API Rate Limiting
- Error Handling

---

## 2. Project Folder Structure

```text
StockTracker/
│
├── manage.py
│
├── StockTracker/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── finnhub_app/
│   ├── migrations/
│   ├── templates/
│   │   ├── home.html
│   │   ├── stocks.html
│   │   ├── login.html
│   │   └── register.html
│   │
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── services.py
│   ├── urls.py
│   └── views.py
│
└── requirements.txt
```

---

## 3. Install Dependencies

```bash
pip install django
pip install requests
pip install django-ratelimit
```

Save dependencies:

```bash
pip freeze > requirements.txt
```

---

## 4. Database Models – models.py

The project uses two main models:

- Stock: Stores stock symbols and prices.
- Portfolio: Stores the stocks belonging to a user.

Example implementation:

```python
from django.db import models
from django.contrib.auth.models import User


class Stock(models.Model):
    symbol = models.CharField(
        max_length=20,
        unique=True
    )

    price = models.DecimalField(
        max_digits=15,
        decimal_places=4
    )

    def __str__(self):
        return self.symbol


class Portfolio(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    stocks = models.ManyToManyField(
        Stock,
        blank=True
    )

    def __str__(self):
        return f"{self.user.username}'s Portfolio"
```

### Explanation

**Stock Model**

Stores:
- Stock symbol
- Stock price

**Portfolio Model**

Stores:
- User relationship
- Multiple stocks

The `ManyToManyField` allows a portfolio to contain multiple stocks.

The `OneToOneField` ensures that each user has one portfolio.

---

## 5. User Registration Form – forms.py

```python
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserRegistrationForm(UserCreationForm):

    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password1",
            "password2"
        ]
```

### Explanation

`UserCreationForm` provides:
- Username validation
- Password validation
- Password confirmation
- Secure password hashing through Django

---

## 6. Finnhub API Service – services.py

This module communicates with the external Finnhub API.

```python
import os
import requests


def get_stock_data(symbol):

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
```

### Explanation

The `get_stock_data()` function:

1. Receives a stock symbol.
2. Validates the symbol.
3. Reads the Finnhub API key.
4. Sends an HTTP GET request.
5. Receives JSON data.
6. Extracts the current price.
7. Returns stock data or an error.

### Finnhub Quote API

```text
https://finnhub.io/api/v1/quote
```

Important response fields:

| Field | Meaning |
|---|---|
| c | Current price |
| d | Change |
| dp | Percentage change |
| h | High price |
| l | Low price |
| o | Open price |
| pc | Previous close |
| t | Timestamp |

---

## 7. Django Views – views.py

The views module handles all application requests.

### Import Statements

```python
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import ensure_csrf_cookie
from django_ratelimit.decorators import ratelimit

from .models import Stock, Portfolio
from .forms import UserRegistrationForm
from .services import get_stock_data
```

### A. Home View

```python
@login_required
@ensure_csrf_cookie
def home(request):

    portfolio, created = Portfolio.objects.get_or_create(
        user=request.user
    )

    return render(
        request,
        "stocks.html",
        {"portfolio": portfolio}
    )
```

**Purpose:**
- Requires authentication.
- Creates a portfolio if one does not exist.
- Renders the dashboard.

### B. Registration View

```python
@ratelimit(key="ip", rate="5/m", block=True)
def register(request):

    if request.method == "POST":

        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("login")

    else:
        form = UserRegistrationForm()

    return render(
        request,
        "register.html",
        {"form": form}
    )
```

**Purpose:**
- Handles user registration.
- Validates registration data.
- Saves the new user.
- Redirects to login.

### C. Add Stock View

```python
@login_required
@ratelimit(key="ip", rate="60/m", block=True)
@require_POST
def fetch_stock_data(request):

    symbol = request.POST.get(
        "symbol", ""
    ).strip().upper()

    if not symbol:
        return JsonResponse({
            "success": False,
            "error": "Stock symbol is required."
        }, status=400)

    try:

        data, error = get_stock_data(symbol)

        if error:
            return JsonResponse({
                "success": False,
                "error": error
            }, status=400)

        price = data.get("c")

        if price is None or price <= 0:
            return JsonResponse({
                "success": False,
                "error": "Invalid stock price."
            }, status=400)

        stock, created = Stock.objects.get_or_create(
            symbol=symbol,
            defaults={"price": price}
        )

        portfolio, created = Portfolio.objects.get_or_create(
            user=request.user
        )

        if portfolio.stocks.filter(pk=stock.pk).exists():

            return JsonResponse({
                "success": False,
                "error": f"{symbol} is already in your portfolio."
            }, status=409)

        if not created:
            stock.price = price
            stock.save(update_fields=["price"])

        portfolio.stocks.add(stock)

        return JsonResponse({
            "success": True,
            "message": f"{symbol} added successfully.",
            "symbol": stock.symbol,
            "price": stock.price
        })

    except Exception:

        return JsonResponse({
            "success": False,
            "error": "Something went wrong while adding stock."
        }, status=500)
```

**Purpose:**

1. Receives stock symbol.
2. Fetches stock data from Finnhub.
3. Checks whether the stock already exists in the user's portfolio.
4. Creates or updates the Stock record.
5. Adds the stock to the user's portfolio.
6. Returns JSON response.

### D. Delete Stock View

```python
@login_required
@require_POST
def delete_stock(request):

    symbol = request.POST.get(
        "symbol", ""
    ).strip().upper()

    if not symbol:
        return JsonResponse({
            "success": False,
            "error": "Stock symbol is required."
        }, status=400)

    portfolio, created = Portfolio.objects.get_or_create(
        user=request.user
    )

    try:
        stock = Stock.objects.get(symbol=symbol)

    except Stock.DoesNotExist:

        return JsonResponse({
            "success": False,
            "error": "Stock not found."
        }, status=404)

    if not portfolio.stocks.filter(pk=stock.pk).exists():

        return JsonResponse({
            "success": False,
            "error": "Stock is not in your portfolio."
        }, status=404)

    portfolio.stocks.remove(stock)

    return JsonResponse({
        "success": True,
        "message": f"Stock {symbol} removed successfully."
    })
```

**Purpose:**

Removes a stock from the current user's portfolio.

It does not delete the global Stock database record.

### E. Stock Data API

```python
@login_required
@ratelimit(key="ip", rate="60/m", block=True)
@require_GET
def stock_data_api(request):

    portfolio, created = Portfolio.objects.get_or_create(
        user=request.user
    )

    stocks = portfolio.stocks.all().order_by("symbol")

    data = [
        {
            "symbol": stock.symbol,
            "price": stock.price
        }
        for stock in stocks
    ]

    return JsonResponse(data, safe=False)
```

**Purpose:**

Returns all stocks belonging to the authenticated user.

Example JSON response:

```json
[
    {
        "symbol": "AAPL",
        "price": "225.5000"
    },
    {
        "symbol": "MSFT",
        "price": "450.2500"
    }
]
```

### F. Refresh Stock Prices

```python
@login_required
@ratelimit(key="ip", rate="60/m", block=True)
@require_POST
def refresh_stock_prices(request):

    portfolio, created = Portfolio.objects.get_or_create(
        user=request.user
    )

    stocks = portfolio.stocks.all()

    updated = []
    errors = []

    for stock in stocks:

        data, error = get_stock_data(stock.symbol)

        if error:
            errors.append({
                "symbol": stock.symbol,
                "error": error
            })
            continue

        price = data.get("c")

        if price is None or price <= 0:
            errors.append({
                "symbol": stock.symbol,
                "error": "Invalid stock price."
            })
            continue

        stock.price = price

        stock.save(update_fields=["price"])

        updated.append({
            "symbol": stock.symbol,
            "price": stock.price
        })

    return JsonResponse({
        "success": True,
        "updated": updated,
        "errors": errors
    })
```

**Purpose:**

Fetches updated prices from Finnhub for every stock in the user's portfolio.

---

## 8. URL Configuration – urls.py

```python
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from . import views


urlpatterns = [

    path("", views.home, name="home"),

    path(
        "login/",
        LoginView.as_view(template_name="login.html"),
        name="login"
    ),

    path(
        "logout/",
        LogoutView.as_view(),
        name="logout"
    ),

    path(
        "register/",
        views.register,
        name="register"
    ),

    path(
        "stock-data/",
        views.fetch_stock_data,
        name="fetch_stock_data"
    ),

    path(
        "api/stock-data/",
        views.stock_data_api,
        name="stock_data_api"
    ),

    path(
        "delete-stock/",
        views.delete_stock,
        name="delete_stock"
    ),

    path(
        "refresh-stock-prices/",
        views.refresh_stock_prices,
        name="refresh_stock_prices"
    ),

]
```

---

## 9. Frontend – stocks.html

The frontend uses JavaScript Fetch API to communicate with Django.

### Main Responsibilities

- Add stock through AJAX.
- Load portfolio data.
- Delete stock.
- Refresh stock prices.
- Show success and error messages.
- Automatically refresh dashboard display.

### Important JavaScript Concepts

**Fetch API**

Used to send HTTP requests from JavaScript.

```javascript
fetch('/api/stock-data/')
    .then(response => response.json())
    .then(data => {
        console.log(data);
    });
```

**POST Request**

Used to submit stock symbols.

```javascript
fetch('/stock-data/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-CSRFToken': csrfToken
    },
    body: new URLSearchParams({
        symbol: 'AAPL'
    })
});
```

**DOM Manipulation**

Used to update HTML elements dynamically.

```javascript
document.getElementById('message').textContent =
    'Stock added successfully!';
```

**Auto Refresh**

```javascript
setInterval(updateDashboard, 60000);
```

This refreshes the dashboard display every 60 seconds.

Important: This only reloads database data. It does not automatically fetch fresh Finnhub prices.

---

## 10. API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Dashboard |
| GET | `/login/` | Login page |
| POST | `/login/` | Authenticate user |
| POST | `/logout/` | Logout |
| GET/POST | `/register/` | Registration |
| POST | `/stock-data/` | Add stock |
| GET | `/api/stock-data/` | Get portfolio stocks |
| POST | `/delete-stock/` | Delete stock from portfolio |
| POST | `/refresh-stock-prices/` | Refresh prices |

---

## 11. Important Error: 400 Bad Request

### Original Console Error

```text
POST /stock-data/ 400 (Bad Request)
```

### Why It Happened

The original JavaScript contained this logic:

```javascript
const symbols = data.map(stock => stock.symbol);

const fetchPromises = symbols.map(symbol => {
    return fetch('/stock-data/', {
        method: 'POST',
        body: `symbol=${encodeURIComponent(symbol)}`
    });
});
```

This was incorrect.

### Explanation

1. Dashboard loaded portfolio stocks.
2. JavaScript retrieved all stock symbols.
3. JavaScript sent another POST request for every existing stock.
4. Django checked whether the stock was already in the portfolio.
5. Django rejected the duplicate request.

### Correct Solution

Dashboard loading should only fetch data:

```javascript
async function updateDashboard() {

    const response = await fetch('/api/stock-data/');

    const data = await response.json();

    console.log(data);

}
```

Stock adding should happen only when the user submits the Add Stock form.

---

## 12. HTTP Status Codes

| Status | Meaning |
|---|---|
| 200 | Request successful |
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 409 | Conflict / Duplicate |
| 429 | Too Many Requests |
| 500 | Internal Server Error |

### Important Difference

- 400: Invalid request data.
- 404: Requested resource not found.
- 409: Conflict, such as a duplicate stock.
- 500: Unexpected server-side error.

---

## 13. Security Features

### Authentication

```python
@login_required
```

Ensures that only authenticated users can access protected views.

### CSRF Protection

```html
{% csrf_token %}
```

Protects POST requests against Cross-Site Request Forgery.

### Rate Limiting

```python
@ratelimit(key="ip", rate="60/m", block=True)
```

Limits the number of requests from an IP address.

### Environment Variables

```python
api_key = os.getenv("FINNHUB_API_KEY")
```

Keeps API keys outside the source code.

### User-Specific Portfolio

```python
Portfolio.objects.get_or_create(
    user=request.user
)
```

Ensures that each authenticated user works with their own portfolio.

---

## 14. Environment Configuration

Windows CMD:

```bash
set FINNHUB_API_KEY=your_actual_api_key
```

PowerShell:

```powershell
$env:FINNHUB_API_KEY="your_actual_api_key"
```

Start server:

```bash
python manage.py runserver
```

Never upload your actual API key to GitHub.

---

## 15. Database Commands

Create migrations:

```bash
python manage.py makemigrations
```

Apply migrations:

```bash
python manage.py migrate
```

Create superuser:

```bash
python manage.py createsuperuser
```

Check project:

```bash
python manage.py check
```

Start development server:

```bash
python manage.py runserver
```

---

## 16. Testing Checklist

- [ ] Register a new user.
- [ ] Login successfully.
- [ ] Open the dashboard.
- [ ] Add AAPL stock.
- [ ] Verify stock price.
- [ ] Try adding AAPL again.
- [ ] Confirm duplicate protection.
- [ ] Add another stock.
- [ ] Refresh stock prices.
- [ ] Delete a stock.
- [ ] Verify deleted stock disappears.
- [ ] Logout successfully.
- [ ] Verify unauthenticated users cannot access dashboard APIs.
- [ ] Check browser console for errors.

---

## 17. Interview Questions and Answers

### Q1. What is Django?

Django is a high-level Python web framework used to build secure and maintainable web applications quickly.

### Q2. What is an API?

An API (Application Programming Interface) allows two software systems to communicate with each other.

### Q3. What is JSON?

JSON (JavaScript Object Notation) is a lightweight data-interchange format.

### Q4. What is JsonResponse?

`JsonResponse` is a Django class used to return JSON data to clients.

### Q5. What is ManyToManyField?

It creates a many-to-many relationship between two database models.

### Q6. What is OneToOneField?

It creates a one-to-one relationship between two models.

### Q7. What is get_or_create()?

It retrieves an existing database object or creates a new one if it does not exist.

### Q8. What is CSRF?

Cross-Site Request Forgery is an attack that tricks authenticated users into submitting unwanted requests.

### Q9. What is rate limiting?

Rate limiting restricts how many requests a client can make within a specified period.

### Q10. What is AJAX?

AJAX allows web pages to communicate with servers asynchronously without reloading the entire page.

### Q11. What is the difference between GET and POST?

GET retrieves data, while POST submits data to the server.

### Q12. Why use environment variables?

They help keep sensitive configuration values, such as API keys, outside the source code.

### Q13. What is the purpose of a service layer?

A service layer separates business logic and external API communication from Django views.

### Q14. Why did the original application return 400?

Because the dashboard attempted to add stocks that were already present in the user's portfolio.

### Q15. How is the issue fixed?

By separating the dashboard data-fetching operation from the stock-adding operation.

---

## 18. Final Project Architecture

```text
                 USER
                  |
                  v
             Django Views
                  |
          ------------------
          |                |
          v                v
      Add Stock        Dashboard API
          |                |
          v                v
      Services          Database
          |
          v
      Finnhub API
          |
          v
      Stock Price
          |
          v
       Database
          |
          v
     Dashboard UI
```

### Key Takeaways

1. Django views handle HTTP requests.
2. Models handle database structure.
3. Services handle external API communication.
4. URLs connect requests to views.
5. JavaScript updates the frontend dynamically.
6. CSRF protects POST requests.
7. Authentication protects private user data.
8. Rate limiting controls request frequency.
9. Duplicate checking prevents repeated portfolio entries.
10. Separating responsibilities makes the application easier to maintain.

**Project Status:** Core stock tracking functionality implemented. Further improvements can include automated background updates, unit tests, transaction-safe stock operations, caching, and production deployment.
