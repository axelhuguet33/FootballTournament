# Football Tournament

Ce projet est une application Django pour gérer un tournoi de football. Il permet de créer des équipes, des joueurs, d'organiser des matchs et de visualiser le classement des équipes.

## Fonctionnalités

- **Gestion des équipes** : Créez et gérez les équipes de football.
- **Gestion des joueurs** : Ajoutez des joueurs aux équipes.
- **Organisation des matchs** : Planifiez des matchs entre les équipes.
- **Classement des équipes** : Affichez le classement des équipes basé sur les résultats des matchs.

## Prérequis

- Python 3.8+
- Django 3.2+
- PostgreSQL

## Installation

1. Installez Python :
sudo apt-get update
sudo apt-get install python3 python3-venv python3-pip
   
2. Installez PostgreSQL :
sudo apt-get install postgresql postgresql-contrib

3. Clonez le dépôt :
git clone https://github.com/axelhuguet33/FootballTournament.git
cd FootballTournament

4. Créez et activez un environnement virtuel :
python3 -m venv .venv
source .venv/bin/activate

5. Installez les dépendances :
pip install -r requirements.txt

6. Configurez la base de données PostgreSQL dans settings.py.

7. Appliquez les migrations :
python manage.py migrate

8. Lancez le serveur de développement :
python manage.py runserver

9. Accédez à l'application dans votre navigateur :
http://127.0.0.1:8000/

### Tests

Pour exécuter les tests, utilisez la commande suivante :
python manage.py test
