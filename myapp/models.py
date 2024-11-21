from django.db import models
from django.core.exceptions import ValidationError

class Equipe(models.Model):
    nom = models.CharField(max_length=50)
    ville = models.CharField(max_length=100)

    def __str__(self):
        return self.nom

    @property
    def points(self):
        matches_home = self.home_matches.all()
        matches_away = self.away_matches.all()
        points = 0
        for match in matches_home:
            if match.buts_equipe1 > match.buts_equipe2:
                points += 3
            elif match.buts_equipe1 == match.buts_equipe2:
                points += 1
        for match in matches_away:
            if match.buts_equipe2 > match.buts_equipe1:
                points += 3
            elif match.buts_equipe2 == match.buts_equipe1:
                points += 1
        return points

    @property
    def buts_marques(self):
        matches_home = self.home_matches.all()
        matches_away = self.away_matches.all()
        buts = sum(match.buts_equipe1 for match in matches_home) + sum(match.buts_equipe2 for match in matches_away)
        return buts

class Joueur(models.Model):
    POSTE_CHOICES = [
        ('Gardien', 'Gardien'),
        ('Défenseur', 'Défenseur'),
        ('Milieu', 'Milieu'),
        ('Attaquant', 'Attaquant'),
    ]
    nom = models.CharField(max_length=100)
    poste = models.CharField(max_length=10, choices=POSTE_CHOICES)
    equipe = models.ForeignKey(Equipe, on_delete=models.CASCADE)

    def clean(self):
        if self.equipe and Joueur.objects.filter(equipe=self.equipe).count() >= 11:
            raise ValidationError("L'équipe a déjà 11 joueurs.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nom
    
class Match(models.Model):
    equipe1 = models.ForeignKey(Equipe, related_name='home_matches', on_delete=models.CASCADE)
    equipe2 = models.ForeignKey(Equipe, related_name='away_matches', on_delete=models.CASCADE)
    buts_equipe1 = models.PositiveIntegerField()
    buts_equipe2 = models.PositiveIntegerField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.equipe1} vs {self.equipe2}"