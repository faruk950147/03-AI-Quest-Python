from django.urls import path
from task.views import (
    HomeView, EditedView, IsCompleteView, DeletedView
)

urlpatterns = [
    path("", HomeView.as_view(), name="HomeView"),
    path("EditedView/<int:id>", EditedView.as_view(), name="EditedView"),
    path("IsCompleteView/<int:id>", IsCompleteView.as_view(), name="IsCompleteView"),
    path("DeletedView/<int:id>", DeletedView.as_view(), name="DeletedView"),
]
