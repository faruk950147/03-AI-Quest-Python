from django.urls import path
from Deap_learning.views import Deap_learning
urlpatterns = [
    path('deap_learning/', Deap_learning.as_view(), name='deap_learning'),
]
