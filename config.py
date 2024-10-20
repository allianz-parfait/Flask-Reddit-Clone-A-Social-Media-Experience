# Ici on aura toutes les configurations de l'application

import os

# On met le debug à true
DEBUG = 1

APP_NAME = "REDDIT"

BASEDIR = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASEDIR, "Reddit.sqlite")}"

SQLALCHEMY_TRACK_MODIFICATIONS = False # Pour qu'il évite de faire des modif à chaque fois

SECRET_KEY = "HereIsMySecretKey" # Clé Secrète

STATIC_FOLDER = 'static'

# Chemin vers le dossier statique absolu
STATIC_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), STATIC_FOLDER)

