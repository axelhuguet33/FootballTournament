# tests.py
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.core.exceptions import ValidationError
from .models import Equipe, Joueur

class EquipeModelTest(TestCase):
    def setUp(self):
        self.equipe = Equipe.objects.create(nom="Equipe A", ville="Ville A")

    def test_equipe_creation(self):
        self.assertEqual(self.equipe.nom, "Equipe A")
        self.assertEqual(self.equipe.ville, "Ville A")

class JoueurModelTest(TestCase):
    def setUp(self):
        self.equipe = Equipe.objects.create(nom="Equipe A", ville="Ville A")

    def test_joueur_creation(self):
        joueur = Joueur.objects.create(nom="Joueur 1", poste="Attaquant", equipe=self.equipe)
        self.assertEqual(joueur.nom, "Joueur 1")
        self.assertEqual(joueur.poste, "Attaquant")
        self.assertEqual(joueur.equipe, self.equipe)

    def test_joueur_limite(self):
        for i in range(11):
            Joueur.objects.create(nom=f"Joueur {i+1}", poste="Attaquant", equipe=self.equipe)
        with self.assertRaises(ValidationError):
            joueur = Joueur(nom="Joueur 12", poste="Attaquant", equipe=self.equipe)
            joueur.clean()

class EquipeAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.equipe_url = reverse('equipe-list-create')
        self.joueur_url = reverse('joueur-list-create')
        self.equipe = Equipe.objects.create(nom="Equipe A", ville="Ville A")

    def test_create_equipe(self):
        data = {'nom': 'Equipe B', 'ville': 'Ville B'}
        response = self.client.post(self.equipe_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Equipe.objects.count(), 2)

    def test_create_joueur(self):
        data = {'nom': 'Joueur 1', 'poste': 'Attaquant', 'equipe': self.equipe.id}
        response = self.client.post(self.joueur_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Joueur.objects.count(), 1)

    def test_joueur_limite_api(self):
        for i in range(11):
            Joueur.objects.create(nom=f"Joueur {i+1}", poste="Attaquant", equipe=self.equipe)
        data = {'nom': 'Joueur 12', 'poste': 'Attaquant', 'equipe': self.equipe.id}
        response = self.client.post(self.joueur_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("L'équipe a déjà 11 joueurs.", response.data['non_field_errors'])

class MatchModelTest(TestCase):
    def setUp(self):
        self.equipe1 = Equipe.objects.create(nom="Equipe A", ville="Ville A")
        self.equipe2 = Equipe.objects.create(nom="Equipe B", ville="Ville B")
        self.equipe3 = Equipe.objects.create(nom="Equipe C", ville="Ville C")

    def test_unique_matches(self):
        Match.objects.create(equipe1=self.equipe1, equipe2=self.equipe2, buts_equipe1=2, buts_equipe2=1)
        Match.objects.create(equipe1=self.equipe1, equipe2=self.equipe3, buts_equipe1=1, buts_equipe2=1)
        Match.objects.create(equipe1=self.equipe2, equipe2=self.equipe3, buts_equipe1=0, buts_equipe2=3)

        matches = Match.objects.all()
        self.assertEqual(matches.count(), 3)

        unique_matches = set()
        for match in matches:
            unique_matches.add(frozenset([match.equipe1.id, match.equipe2.id]))
        self.assertEqual(len(unique_matches), matches.count())

class ClassementViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.equipe1 = Equipe.objects.create(nom="Equipe A", ville="Ville A")
        self.equipe2 = Equipe.objects.create(nom="Equipe B", ville="Ville B")
        self.equipe3 = Equipe.objects.create(nom="Equipe C", ville="Ville C")

        Match.objects.create(equipe1=self.equipe1, equipe2=self.equipe2, buts_equipe1=2, buts_equipe2=1)
        Match.objects.create(equipe1=self.equipe1, equipe2=self.equipe3, buts_equipe1=1, buts_equipe2=1)
        Match.objects.create(equipe1=self.equipe2, equipe2=self.equipe3, buts_equipe1=0, buts_equipe2=3)

    def test_classement_view(self):
        response = self.client.get(reverse('classement'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Equipe A")
        self.assertContains(response, "Equipe B")
        self.assertContains(response, "Equipe C")

        equipes = response.context['equipes']
        equipe1 = equipes.get(nom="Equipe A")
        equipe2 = equipes.get(nom="Equipe B")
        equipe3 = equipes.get(nom="Equipe C")

        self.assertEqual(equipe1.points, 4)
        self.assertEqual(equipe1.buts_marques, 3)

        self.assertEqual(equipe2.points, 0)
        self.assertEqual(equipe2.buts_marques, 1)

        self.assertEqual(equipe3.points, 4)
        self.assertEqual(equipe3.buts_marques, 4)