
from django.views import generic
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from mixins.mixing import LoginRequiredMixin, LogoutRequiredMixin

from service.models import Description, Service, StatusChoices

@method_decorator(cache_page(60 * 10), name="get")
class ServiceView(LoginRequiredMixin, generic.View):
    login_url = 'login'

    def get(self, request):
        description = Description.objects.filter(status=StatusChoices.ACTIVE).first()
        services = Service.objects.filter(status=StatusChoices.ACTIVE)

        context = {
            "description": description,
            "services": services,
        }

        return render(request, 'service/service.html', context)