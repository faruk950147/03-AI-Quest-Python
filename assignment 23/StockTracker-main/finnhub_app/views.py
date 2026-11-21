
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import ensure_csrf_cookie
from django_ratelimit.decorators import ratelimit

from .models import Stock, Portfolio
from .forms import UserRegistrationForm
from .services import get_stock_data


@login_required
@ensure_csrf_cookie
def home(request):
    """Render authenticated user's stock portfolio."""

    portfolio, created = Portfolio.objects.get_or_create(
        user=request.user
    )

    return render(
        request,
        "stocks.html",
        {"portfolio": portfolio}
    )


@ratelimit(key="ip", rate="5/m", block=True)
def register(request):
    """User registration."""

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


@login_required
@require_POST
def delete_stock(request):
    """Delete stock from user's portfolio."""

    symbol = request.POST.get("symbol", "").strip().upper()

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


@login_required
@ratelimit(key="ip", rate="60/m", block=True)
@require_POST
def fetch_stock_data(request):
    """Fetch stock data and add it to user's portfolio."""

    symbol = request.POST.get("symbol", "").strip().upper()

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

        # Prevent duplicate stocks in portfolio
        if portfolio.stocks.filter(pk=stock.pk).exists():
            return JsonResponse({
                "success": False,
                "error": f"{symbol} is already in your portfolio."
            }, status=409)

        # Update latest price
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


@login_required
@ratelimit(key="ip", rate="60/m", block=True)
@require_GET
def stock_data_api(request):
    """Return all stocks in authenticated user's portfolio."""

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


@login_required
@ratelimit(key="ip", rate="60/m", block=True)
@require_POST
def refresh_stock_prices(request):
    """Refresh prices of all stocks in user's portfolio."""

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
