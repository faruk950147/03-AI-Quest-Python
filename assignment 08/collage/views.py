from django.shortcuts import render
from django.views import generic
from collage.models import Collage, Department

# Create your views here.
class CollageView(generic.View):
    def get(self, request):
        context = {
            'collages': Collage.objects.filter(status=True),
            'departments': Department.objects.filter(status=True)
        }
        return render(request, "collage/collage.html", context)
    def post(self, request):

        return render(request, "collage/collage.html")