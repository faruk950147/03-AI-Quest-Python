from requests import get
from django.views import generic 
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from account.mixins import LogoutRequiredMixin

User = get_user_model()

 
@method_decorator(never_cache, name='dispatch')
class SignupView(LogoutRequiredMixin, generic.View):
    def get(self, request):
        pass
    def post(self, request):
        pass
    
@method_decorator(never_cache, name='dispatch')
class SignInView(LogoutRequiredMixin, generic.View):
    def get(self, request):
        pass
    def post(self, request):
        pass
    