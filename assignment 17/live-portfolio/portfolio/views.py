from django.shortcuts import render
from django.views import generic
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

from mixins.mixing import LoginRequiredMixin
from portfolio.models import StatusChoices, Description, Portfolio

@method_decorator(cache_page(60 * 10), name="get")
class PortfolioView(LoginRequiredMixin, generic.View):
    login_url = "login"

    def get(self, request):
        description = Description.objects.filter(
            status=StatusChoices.ACTIVE
        ).first()

        portfolios = (
            Portfolio.objects
            .filter(status=StatusChoices.ACTIVE)
            .prefetch_related("galleries")
        )

        context = {
            "description": description,
            "portfolios": portfolios,
        }

        return render(
            request,
            "portfolio/portfolio.html",
            context,
        )