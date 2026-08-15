from django.shortcuts import render
from django.views import generic


class SetCookie(generic.View):
    def get(self, request, *args, **kwargs):
        response = render(request, 'info/info.html')
        response.set_cookie('name', 'Faruk Cse')
        return response


class InfoDetailView(generic.View):
    def get(self, request, *args, **kwargs):
        info_id = kwargs.get('id')

        name = request.COOKIES.get('name', 'Guest')

        context = {
            'info_id': info_id,
            'name': name,
        }
        return render(request, 'info/info-detail.html', context)
