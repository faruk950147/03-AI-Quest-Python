from django.shortcuts import render, redirect
from django.views import View
import random
from Draw.models import Participant

class RaffleDrawView(View):
    def get(self, request):
        participants = Participant.objects.all()
        winner = Participant.objects.filter(is_winner=True).first()
        return render(request, 'Draw/raffle_draw.html', {'participants': participants, 'winner': winner})

    def post(self, request):
        participants = Participant.objects.all()
        if participants.exists():
            # bulk update that is faster than updating one by one when we have all participants is false
            Participant.objects.update(is_winner=False)
            winner = random.choice(list(participants))
            winner.is_winner = True
            winner.save()
            return redirect('raffle_draw')
        else:
            return render(request, 'Draw/raffle_draw.html', {'participants': participants, 'winner': None})

class AddParticipantView(View):
    def get(self, request):
        return render(request, 'Draw/add_participant.html')
    
    def post(self, request):
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        if name and phone and email:
            Participant.objects.create(name=name, phone=phone, email=email)
        return redirect('raffle_draw')

class ParticipantsView(View):
    def get(self, request):
        participants = Participant.objects.all()
        return render(request, 'Draw/participants.html', {'participants': participants})
