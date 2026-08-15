from django.urls import path
from cbv.views import (
    PersonListView,
    PersonInheritView,
    PersonTemplateView,
    PersonRedirectView,
)

urlpatterns = [
    path('', PersonListView.as_view(), name='person_list'),
    path('person-inherit/', PersonInheritView.as_view(), name='person_inherit'),
    path('person-template/', PersonTemplateView.as_view(), name='person_template'),
    path('person-redirect/', PersonRedirectView.as_view(), name='person_redirect'),
]