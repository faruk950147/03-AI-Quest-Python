from django.urls import path
from queryset.views import (
    PostListWithoutSelectRelatedView,
    PostListWithSelectRelatedView,
    PostListWithoutPrefetchRelatedView,
    PostListWithPrefetchRelatedView,
    PostListOptimizedView,
    ShowView,
)

urlpatterns = [
    path('no-select/', PostListWithoutSelectRelatedView.as_view(), name='posts-no-select'),
    path('select/', PostListWithSelectRelatedView.as_view(), name='posts-select'),
    path('no-prefetch/', PostListWithoutPrefetchRelatedView.as_view(), name='posts-no-prefetch'),
    path('prefetch/', PostListWithPrefetchRelatedView.as_view(), name='posts-prefetch'),
    path('optimized/', PostListOptimizedView.as_view(), name='posts-optimized'),
    path('', ShowView.as_view(), name='show'),
]