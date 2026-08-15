from django.urls import path
from .views import RaffleDrawView, AddParticipantView, ParticipantsView     

urlpatterns = [
    path('', ParticipantsView.as_view(), name='participants'),
    path('raffle_draw/', RaffleDrawView.as_view(), name='raffle_draw'),
    path('add_participant/', AddParticipantView.as_view(), name='add_participant'),
    ]
