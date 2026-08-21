from django.urls import path

from resume.views import (
    ResumeView
)

urlpatterns = [
    path('resume/', ResumeView.as_view(), name='resume')
]
