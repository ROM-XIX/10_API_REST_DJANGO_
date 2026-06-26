# SoftDesk — Collection Postman

Collection officielle pour tester l'API SoftDesk en local.

## Import dans Postman

1. Ouvrir Postman → **Import** (en haut à gauche).
2. Glisser-déposer les **2 fichiers** :
   - `softdesk.postman_collection.json` (la collection)
   - `softdesk.postman_environment.json` (l'environnement)
3. Activer l'environnement **SoftDesk local** (sélecteur en haut à droite).

## Pré-requis

- Le serveur Django doit tourner localement : `poetry run python src/manage.py runserver`
- La BD doit être migrée : `poetry run python src/manage.py migrate`

## Ordre d'utilisation recommandé

| # | Requête                                  | Effet                                                 |
|---|-------------------------------------------|--------------------------------------------------------|
| 1 | **Auth → Register Alice**                  | Crée le premier user                                   |
| 2 | **Auth → Register Bob**                    | Crée le second user                                    |
| 3 | **Auth → Login Alice**                     | Récupère access + refresh → **auto-stockés** dans l'env |
| 4 | **Projects → Create project**              | Crée P1 → `projectId` auto-extrait                     |
| 5 | **Contributors → Add contributor (Bob)**    | Ajoute Bob (`user: 2`) au projet                       |
| 6 | **Issues → Create issue**                  | Crée I1 → `issueId` auto-extrait                       |
| 7 | **Comments → Create comment**              | Crée C1 → `commentUuid` auto-extrait                   |
| 8 | Explorer les autres endpoints              | retrieve, patch, delete, list…                         |

→ Après l'étape 7, **toutes les variables sont peuplées** automatiquement.

## Tests de codes HTTP attendus (à montrer en soutenance)

| Test                                                                | Code attendu | Raison                                  |
|---------------------------------------------------------------------|---------------|------------------------------------------|
| **Auth → Register — Refus < 15 ans**                                 | 400           | RGPD article 8                            |
| Auth → Login avec mauvais password                                   | 401           | OWASP A07                                |
| GET `/api/users/` sans Authorization                                  | 401           | OWASP A01                                |
| Login Bob + GET `/api/projects/{id}/` créé par Alice avant invitation | 404           | filtrage queryset (anti-énumération)    |
| Login Bob + PATCH `/api/projects/{id}/` (contributeur pas auteur)     | 403           | OWASP A01 (IsAuthorOrReadOnly)          |
| Alice DELETE son propre projet                                        | 204           | flux normal                              |

## Astuce démo

Pour montrer le **flux complet JWT** :
1. Login → tokens stockés
2. GET un endpoint protégé → 200
3. Refresh token → nouveau couple (rotation visible : refreshToken change)
4. Logout → refresh blacklisté
5. Tenter Refresh à nouveau → **401 "Le jeton a été banni"**

## Modifier les variables

Cliquer sur l'œil en haut à droite (à côté du sélecteur d'environnement) puis "Edit" pour ajuster.

## Forks acceptés

La collection est au format **Postman Collection v2.1**, compatible avec :
- Postman 9+
- Insomnia (import via menu)
- Bruno
- httpie collections (avec conversion)
