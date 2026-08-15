from django.urls import path
from Django_learning.views import DjangoLearningView
urlpatterns = [
    path('django_learning/', DjangoLearningView.as_view(), name='django_learning'),
]
