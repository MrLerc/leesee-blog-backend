# Backend du blog Leesee

API REST pour un blog simple, développée avec Python, Flask, Flask-SQLAlchemy et SQLite.

## Fonctionnalités

- Afficher tous les articles
- Consulter un article par son identifiant
- Créer un article
- Modifier un article
- Supprimer un article
- Valider les champs obligatoires et leur longueur
- Exécuter des tests automatisés de l'API

## Prérequis

- Python 3.11 ou une version plus récente
- pip

## Installation et exécution locale

1. Cloner ce dépôt.
2. Ouvrir un terminal dans le dossier du backend.
3. Créer un environnement virtuel :

   ```bash
   python -m venv .venv
   ```

4. Activer l'environnement virtuel.

   Sous Windows PowerShell :

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

   Sous macOS ou Linux :

   ```bash
   source .venv/bin/activate
   ```

5. Installer les dépendances :

   ```bash
   python -m pip install -r requirements.txt
   ```

6. Démarrer l'API :

   ```bash
   python app.py
   ```

L'API sera accessible à l'adresse `http://127.0.0.1:5000`.

## Points de terminaison de l'API

| Méthode | Adresse | Description |
|---|---|---|
| GET | `/api/posts` | Afficher tous les articles |
| GET | `/api/posts/<id>` | Consulter un article |
| POST | `/api/posts` | Créer un article |
| PUT | `/api/posts/<id>` | Modifier un article |
| DELETE | `/api/posts/<id>` | Supprimer un article |

Pour les requêtes POST et PUT, envoyer un objet JSON contenant les champs `title`, `content` et `author`.

## Exécuter les tests

Avec l'environnement virtuel activé, exécuter :

```bash
python -m unittest -v
```

Les tests utilisent une base de données SQLite temporaire en mémoire.

## Déploiement

Adresse du backend en ligne : à ajouter après le déploiement.

## Technologies utilisées

Python, Flask, Flask-CORS, Flask-SQLAlchemy, SQLite et unittest.