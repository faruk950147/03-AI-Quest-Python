from django.shortcuts import redirect
from django.urls import reverse_lazy


class LogoutRequiredMixin:
    redirect_authenticated_url = reverse_lazy('home')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(self.redirect_authenticated_url)
        return super().dispatch(request, *args, **kwargs)
    
class LoginRequiredMixin:
    login_url = reverse_lazy('sign-in')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(self.login_url)
        return super().dispatch(request, *args, **kwargs)

