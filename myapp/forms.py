from django import forms
from .models import Equipe, Joueur,  Match

class EquipeForm(forms.ModelForm):
    class Meta:
        model = Equipe
        fields = ['nom', 'ville']

class JoueurForm(forms.ModelForm):
    class Meta:
        model = Joueur
        fields = ['nom','poste','equipe']

class MatchForm(forms.ModelForm):
    class Meta:
        model = Match
        fields = ['equipe1', 'equipe2', 'buts_equipe1', 'buts_equipe2']