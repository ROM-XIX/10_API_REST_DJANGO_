.PHONY: help install format lint test precommit clean

help:  ## Afficher cette aide
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2}'

install:  ## Installer toutes les dépendances (Poetry)
	poetry install

format:  ## Formater le code (isort puis Black)
	poetry run isort .
	poetry run black .

lint:  ## Linter le code (Flake8)
	poetry run flake8 .

test:  ## Lancer les tests (pytest)
	poetry run pytest

precommit:  ## Lancer pre-commit sur l'ensemble du repo
	poetry run pre-commit run --all-files

clean:  ## Nettoyer les caches Python/tests
	find . -type d -name '__pycache__' -prune -exec rm -rf {} +
	find . -type d -name '.pytest_cache' -prune -exec rm -rf {} +
	find . -type d -name '.mypy_cache' -prune -exec rm -rf {} +
