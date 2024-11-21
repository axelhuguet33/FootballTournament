from django.urls import path
from .views import EquipeListCreate, equipe_create_view, JoueurListCreate, joueur_create_view, classement_view, match_create_view

urlpatterns = [
    path('equipes/', EquipeListCreate.as_view(), name='equipe-list-create'),
    path('equipes/new/', equipe_create_view, name='equipe-create'),
    path('joueurs/', JoueurListCreate.as_view(), name='joueur-list-create'),
    path('joueurs/new/', joueur_create_view, name='joueur-create'),
    path('classement/', classement_view, name='classement'),
    path('matchs/new/', match_create_view, name='match-create'),
]