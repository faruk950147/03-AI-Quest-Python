from django.urls import path
from crud.views import (
    HomeView, SavedView, DeletedView, EditedView
)

urlpatterns = [
    path("", HomeView.as_view(), name="HomeView"),
    path("SavedView/", SavedView.as_view(), name="SavedView"),
    path("EditedView/", EditedView.as_view(), name="EditedView"),
    path("DeletedView/", DeletedView.as_view(), name="DeletedView"),
]
