
from django.views import generic
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from home.models import StatusChoices, Hero



@method_decorator(cache_page(60 * 10), name="get")
class HomeView(generic.View):
    def get(self, request):
        hero = Hero.objects.filter(status=StatusChoices.ACTIVE).first()
        return render(request, 'home/index.html', {'hero': hero})
