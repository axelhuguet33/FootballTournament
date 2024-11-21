from rest_framework import serializers
from .models import Equipe, Joueur

class EquipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipe
        fields = ['id', 'nom', 'ville']

class JoueurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Joueur
        fields = ['id', 'nom', 'poste', 'equipe']
    
    def validate(self, data):
        equipe = data.get('equipe')
        if equipe.joueur_set.count() >= 11:
            raise serializers.ValidationError("L'équipe a déjà 11 joueurs.", code='non_field_errors')
        return data