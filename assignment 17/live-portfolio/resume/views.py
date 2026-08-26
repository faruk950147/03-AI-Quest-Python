
from django.views import generic
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from resume.models import (
    Description, Resume,
)

@method_decorator(cache_page(60 * 10), name="get")
class ResumeView(generic.View):
    def get(self, request):
        description = Description.objects.filter(status="active").first()
        resume = Resume.objects.filter(status="active").prefetch_related(
            "educations",
            "skills",
            "trainings",
            "projects",
        ).first()

        context = {
            "description": description,
            "resume": resume,
            "educations": resume.educations.all() if resume else [],
            "skills": resume.skills.all() if resume else [],
            "trainings": resume.trainings.all() if resume else [],
            "projects": resume.projects.all() if resume else [],
        }

        return render(request, "resume/resume.html", context)