from django.urls import path
from task.views import HomeView, EditedView, IsCompleteView, DeletedView

urlpatterns = [
    path('', HomeView.as_view(), name='HomeView'),
    path('edit/<int:id>/', EditedView.as_view(), name='EditedView'),
    path('delete/<int:id>/', DeletedView.as_view(), name='DeletedView'),
    path('iscomplete/<int:id>/', IsCompleteView.as_view(), name='IsCompleteView'),
]