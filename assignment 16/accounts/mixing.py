from django.shortcuts import redirect


class LoginRequiredMixin:
    """
    Mixin to check if the user is authenticated.
    """
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

class LogoutRequiredMixin:
    """
    Mixin to check if the user is not authenticated.
    """
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('sign-in')
        return super().dispatch(request, *args, **kwargs)

