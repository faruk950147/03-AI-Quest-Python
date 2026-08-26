
from django.views import generic
from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

from about.models import (
    Reference, StatusChoices, 
    Description, AboutMe, Stat, 
    Skill, Interest, Reference
)

@method_decorator(cache_page(60 * 15), name="dispatch")
class AboutView(generic.View):
    def get(self, request):
        description = Description.objects.filter(status=StatusChoices.ACTIVE).first()
        about_me = AboutMe.objects.filter(status=StatusChoices.ACTIVE).first()
        stats = Stat.objects.filter(status=StatusChoices.ACTIVE)
        skills_left = Skill.objects.filter(status=StatusChoices.ACTIVE)[:4]
        skills_right = Skill.objects.filter(status=StatusChoices.ACTIVE)[4:8]
        interests = Interest.objects.filter(status=StatusChoices.ACTIVE)
        references = Reference.objects.filter(status=StatusChoices.ACTIVE)
        context = {
            'description': description,
            'about_me': about_me,
            'stats': stats,
            'skills_left': skills_left,
            'skills_right': skills_right,
            'interests': interests,
            'references': references,
        }
        return render(request, 'about/about.html', context)
