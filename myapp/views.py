# views.py
from rest_framework import generics
from .models import Equipe, Joueur
from .serializers import EquipeSerializer, JoueurSerializer
from django.shortcuts import render, redirect
from .forms import EquipeForm, JoueurForm, MatchForm

class EquipeListCreate(generics.ListCreateAPIView):
    queryset = Equipe.objects.all()
    serializer_class = EquipeSerializer

class JoueurListCreate(generics.ListCreateAPIView):
    queryset = Joueur.objects.all()
    serializer_class = JoueurSerializer

def equipe_create_view(request):
    if request.method == 'POST':
        form = EquipeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('equipe-list-create')
    else:
        form = EquipeForm()
    return render(request, 'equipe_form.html', {'form': form})

def joueur_create_view(request):
    if request.method == 'POST':
        form = JoueurForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('joueur-list-create')
    else:
        form = JoueurForm()
    return render(request, 'joueur_form.html', {'form': form})

def classement_view(request):
    equipes = list(Equipe.objects.all())
    equipes.sort(key=lambda e: (e.points, e.buts_marques), reverse=True)
    return render(request, 'classement.html', {'equipes': equipes})

def match_create_view(request):
    if request.method == 'POST':
        form = MatchForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('match-create')
    else:
        form = MatchForm()
    return render(request, 'match_form.html', {'form': form})