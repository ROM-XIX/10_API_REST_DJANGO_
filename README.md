# SoftDesk Support API

API REST sécurisée pour le suivi de problèmes techniques (B2B), développée avec **Django 6** et **Django REST Framework** dans le cadre du projet 10 de la formation OpenClassrooms "Développeur d'application Python".

Conforme aux exigences **OWASP**, **RGPD** et **Green Code**.

## Stack

| Composant                              | Version   |
|----------------------------------------|-----------|
| Python                                  | ≥ 3.12    |
| Django                                  | 6.0.x     |
| Django REST Framework                   | 3.17.x    |
| djangorestframework-simplejwt           | 5.5.x     |
| drf-nested-routers                      | 0.94.x    |
| python-dotenv                           | 1.2.x     |
| BD (dev)                                | SQLite    |
| Gestion dépendances                     | Poetry    |
| Qualité code                            | Black + isort + Flake8 + pre-commit |
| Tests                                   | pytest + pytest-django |

## Pré-requis

- **Python 3.12+** installé sur votre machine
- **Poetry** installé : [https://python-poetry.org/docs/#installation](https://python-poetry.org/docs/#installation)
- **Git** installé

## Installation

```bash
# 1. Cloner le repository
git clone <url-du-repo>
cd <repo>

# 2. Installer les dépendances (création automatique du venv dans .venv/)
poetry install

# 3. Créer le fichier .env à partir du template
cp .env.example .env
# Puis générer une SECRET_KEY :
poetry run python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
# Remplacer la valeur dans .env

# 4. Appliquer les migrations
poetry run python src/manage.py migrate

# 5. (Optionnel) Créer un superuser pour l'admin Django
poetry run python src/manage.py createsuperuser
```

## Lancement

```bash
poetry run python src/manage.py runserver
```

Le serveur démarre sur **http://localhost:8000**.

API root : http://localhost:8000/api/
Admin Django : http://localhost:8000/admin/

## Tests

```bash
poetry run pytest
# ou via make
make test
```

5 tests d'intégration couvrent les chemins critiques (RGPD, JWT, permissions matrice).

## Qualité du code

```bash
make format    # Black + isort
make lint      # Flake8
make precommit # pre-commit sur tout le repo
```

Les hooks pre-commit (Black, isort, Flake8, check-yaml, check-toml) sont activés automatiquement à chaque commit.

## Endpoints — Vue d'ensemble

| URL                                                            | Verbes              | Vue                   |
|---------------------------------------------------------------|----------------------|-----------------------|
| `/api/auth/register/`                                          | POST                 | Inscription publique  |
| `/api/auth/login/`                                             | POST                 | Login JWT             |
| `/api/auth/login/refresh/`                                     | POST                 | Refresh JWT           |
| `/api/auth/logout/`                                            | POST                 | Logout (blacklist)    |
| `/api/users/`                                                  | GET, POST            | Liste / create user   |
| `/api/users/{id}/`                                             | GET, PUT, PATCH, DELETE | CRUD profil utilisateur |
| `/api/projects/`                                               | GET, POST            | Liste / create projet |
| `/api/projects/{id}/`                                          | GET, PUT, PATCH, DELETE | CRUD projet            |
| `/api/projects/{project_pk}/users/`                            | GET, POST            | Gestion contributeurs |
| `/api/projects/{project_pk}/users/{id}/`                       | DELETE               | Retrait contributeur  |
| `/api/projects/{project_pk}/issues/`                           | GET, POST            | Liste / create issue  |
| `/api/projects/{project_pk}/issues/{id}/`                      | GET, PUT, PATCH, DELETE | CRUD issue            |
| `/api/projects/{project_pk}/issues/{issue_pk}/comments/`       | GET, POST            | Liste / create comment |
| `/api/projects/{project_pk}/issues/{issue_pk}/comments/{uuid}/` | GET, PUT, PATCH, DELETE | CRUD comment (UUID)   |

**Pour tester en interactif** : importer la [collection Postman](./postman/README.md) (`postman/softdesk.postman_collection.json` + `softdesk.postman_environment.json`).

## Sécurité

### OWASP Top 10 — risques traités

| Risque                                       | Mitigation                                                              |
|----------------------------------------------|-------------------------------------------------------------------------|
| **A01** Broken Access Control                | `IsAuthenticated` global + `IsAuthorOrReadOnly` + `IsProjectAuthor` + filtrage queryset par contributeur. **Matrice 4 rôles × actions validée par 26 tests** |
| **A02** Cryptographic Failures               | `SECRET_KEY` dans `.env` (gitignored) · password hashé PBKDF2 1.2M itérations · password write_only |
| **A03** Injection                             | ORM Django (jamais `.raw()`)                                            |
| **A07** Identification & Auth Failures        | JWT access court (15 min) + refresh long (7 jours) + rotation + blacklist · password validators Django |

### RGPD

| Article                  | Implémentation                                                    |
|--------------------------|-------------------------------------------------------------------|
| Article 8 (≥ 15 ans)     | `validate_age` dans `RegisterSerializer`                          |
| Article 7 (consentement) | Champs `can_be_contacted` + `can_data_be_shared` (default=False)  |
| Article 17 (droit à l'oubli) | DELETE `/users/{id}/` → CASCADE sur projets/issues/comments + SET_NULL sur assignee |

## Performance (Green Code)

| Métrique                                             | Valeur                              |
|------------------------------------------------------|-------------------------------------|
| Pagination par défaut                                | 10 objets/page                      |
| Requêtes SQL pour un Detail Project (21 contributeurs nested) | **3** (vs 23 sans `select_related` → gain ×7) |
| Imbrication JSON max                                  | 1 niveau (CDC §6.2)                 |
| Sérialiseurs                                         | List léger + Detail enrichi (Green Code) |

## Structure du projet

```
   repo/
   ├── pyproject.toml             ← dépendances Poetry (format PEP 621)
   ├── pytest.ini                  ← config pytest
   ├── Makefile                    ← raccourcis (format, lint, test, run)
   ├── .env.example                ← template variables d'env
   ├── .pre-commit-config.yaml     ← hooks Black/isort/Flake8
   ├── .flake8                     ← config Flake8 (ligne 119)
   ├── .gitignore                  ← exclut .env, .venv, db.sqlite3
   ├── .github/
   │   └── dependabot.yml          ← surveillance des deps (activé après push)
   ├── postman/                    ← collection Postman + environnement
   │   ├── softdesk.postman_collection.json
   │   ├── softdesk.postman_environment.json
   │   └── README.md
   └── src/
       ├── manage.py
       ├── softdesk/               ← config projet (settings, urls, wsgi)
       ├── authentication/         ← User custom + RGPD + register
       ├── projects/               ← Project + Contributor + permissions
       ├── issues/                 ← Issue (BUG/FEATURE/TASK + LOW/MED/HIGH)
       ├── comments/               ← Comment (UUID v4)
       └── tests/                   ← tests pytest
```

## Workflow contributeur

```bash
# Travailler sur une nouvelle feature
git checkout -b feature/ma-feature
# ... coder ...
make format && make lint && make test
git add . && git commit -m "feature: description courte"
git push origin feature/ma-feature
# Ouvrir une PR
```

Les hooks pre-commit vérifient automatiquement Black, isort, Flake8 à chaque commit.

## Licence

Projet pédagogique — usage formation OpenClassrooms.
