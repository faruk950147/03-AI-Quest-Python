from django.shortcuts import render
from django.views import generic


class CacheView(generic.View):
    def get(self, request, *args, **kwargs):
        pass



class InfoDetailView(generic.View):
    def get(self, request, *args, **kwargs):

        return render(request, 'info/info-detail.html', context)
