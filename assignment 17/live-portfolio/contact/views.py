from django.contrib import messages
from django.views import generic
from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from mixins.mixing import LoginRequiredMixin, LogoutRequiredMixin

from contact.models import Description, ContactInfo, StatusChoices
from contact.forms import ContactMeForm

@method_decorator(cache_page(60 * 10), name="get")
class ContactView(LoginRequiredMixin, generic.View):
    login_url = 'login'
    def get(self, request):
        description = Description.objects.filter(status=StatusChoices.ACTIVE).first()
        contact_info = ContactInfo.objects.filter(status=StatusChoices.ACTIVE)
        form = ContactMeForm()
        context = {
            'description': description,
            'contact_info': contact_info,
            'form': form,
        }
        return render(request, 'contact/contact.html', context)
    def post(self, request):
        description = Description.objects.filter(status=StatusChoices.ACTIVE).first()
        contact_info = ContactInfo.objects.filter(status=StatusChoices.ACTIVE)
        form = ContactMeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent successfully.')
        else:
            messages.error(request, 'There was an error sending your message. Please try again.')
        context = {
            'description': description,
            'contact_info': contact_info,
            'form': form,
        }
        return render(request, 'contact/contact.html', context)
