from django.shortcuts import redirect

class LogoutRequiredMixin(object):
    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('sign_in')

        return super(LogoutRequiredMixin, self).dispatch(*args, **kwargs)