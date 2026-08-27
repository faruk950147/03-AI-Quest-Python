from django.shortcuts import render
from django.views import generic
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

from portfolio.models import StatusChoices, Description, Portfolio

@method_decorator(cache_page(60 * 10), name="get")
class PortfolioView(generic.View):

    def get(self, request):
        description = Description.objects.filter(
            status=StatusChoices.ACTIVE
        ).first()

        portfolios = (
            Portfolio.objects
            .filter(status=StatusChoices.ACTIVE)
            .prefetch_related("galleries")
        )
        portfolio_types = Portfolio.TYPES_CHOICES

        context = {
            "description": description,
            "portfolios": portfolios,
            "portfolio_types": portfolio_types
            
        }

        return render(request, "portfolio/portfolio.html", context)