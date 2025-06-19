# Présentation du projet:

Ce projet a pour but de :

- Automatiser l’extraction de données à partir de l’API publique de GitHub.

- Structurer, filtrer et enrichir ces données pour les rendre exploitables.

- Exposer les résultats via une API REST sécurisée développée avec FastAPI, afin de permettre leur consommation par d'autres services ou applications.

# Technologies et outils

Langage : Python

API tierce : GitHub REST API v3

Framework API : FastAPI

Sécurité : Authentification par token (OAuth2 / JWT)

Stockage : JSON 

Tests : Pytest

Documentation automatique : Swagger (généré par FastAPI)

# Fonctionnement général

1. Étape 1 — Extraction automatisée des utilisateurs GitHub via API publique
Le script Python extract_users.py permet d'extraire des données depuis l’API publique de GitHub et les enregister dans un fichier JSON (`data/users.json`).

2. Étape 2 — Structuration et filtrage des utilisateurs extraits 

Une fois de nombreux utilisateurs sont extraits depuis l’API GitHub et enregistrés, le script filtered_users.py:

- lit les données du fichier `users.json`,
- supprime les doublons,
- applique des filtres métiers simples,
- et enregistre un fichier nettoyé nommé `filtered_users.json`. 

3. Étape 3 — Création d’une API REST pour exposer les utilisateurs filtrés

Maintenant que les données ont été nettoyées et filtrées, l'API REST permet d’accéder à ces utilisateurs de manière sécurisée: de consulter la liste des utilisateurs, d’obtenir les détails d’un utilisateur spécifique, et d’effectuer des recherches par mot-clé.

Pour ce faire, **FastAPI** un framework Python léger et moderne est utilisé pour la création de l'API dans le dossier api.



# Structure du projet:


├── extract_users.py               # Script d'extraction depuis l’API GitHub
├── filtered_users.py              # Script de filtrage métier
├── data/
│   ├── users.json                 # Données brutes extraites
│   └── filtered_users.json        # Données nettoyées et filtrées
├── api/
│   ├── main.py                    # Lancement de l’API FastAPI
│   ├── models.py                  # Schémas Pydantic
│   ├── routes.py                  # Endpoints API
│   ├── security.py                # Gestion de l’authentification
├── tests/
│   └── test_api.py                # Tests 
├── requirements.txt              # Dépendances du projet
├── .env.example                  # Exemple de fichier d’environnement
└── README.md                     # Documentation complète du projet