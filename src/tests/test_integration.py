"""Tests d'intégration des chemins critiques SoftDesk."""

import json

import pytest
from django.contrib.auth import get_user_model
from django.test import Client

User = get_user_model()


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def alice(db):
    return User.objects.create_user(
        username="alice",
        password="verysecret123",
        email="a@a.com",
        age=25,
        can_be_contacted=False,
        can_data_be_shared=False,
    )


@pytest.fixture
def bob(db):
    return User.objects.create_user(
        username="bob",
        password="verysecret123",
        email="b@b.com",
        age=30,
        can_be_contacted=False,
        can_data_be_shared=False,
    )


def _login(client, username):
    r = client.post(
        "/api/auth/login/",
        json.dumps({"username": username, "password": "verysecret123"}),
        content_type="application/json",
    )
    return {"HTTP_AUTHORIZATION": f"Bearer {r.json()['access']}"}


def test_register_refuses_under_15(client, db):
    """RGPD : un user de 14 ans ne peut pas s'inscrire."""
    r = client.post(
        "/api/auth/register/",
        json.dumps(
            {
                "username": "kid",
                "email": "k@k.com",
                "password": "verysecret123",
                "age": 14,
                "can_be_contacted": False,
                "can_data_be_shared": False,
            }
        ),
        content_type="application/json",
    )
    assert r.status_code == 400
    assert "age" in r.json()


def test_login_returns_jwt_pair(client, alice):
    """Auth : login retourne access + refresh."""
    r = client.post(
        "/api/auth/login/",
        json.dumps({"username": "alice", "password": "verysecret123"}),
        content_type="application/json",
    )
    assert r.status_code == 200
    assert "access" in r.json()
    assert "refresh" in r.json()


def test_protected_endpoint_requires_bearer(client, alice):
    """OWASP A01 : endpoint protégé sans Bearer → 401."""
    r = client.get("/api/users/")
    assert r.status_code == 401


def test_non_author_cannot_modify_project(client, alice, bob):
    """OWASP A01 (matrice rôles) : contributeur pas auteur → 403 sur PATCH."""
    alice_auth = _login(client, "alice")
    bob_auth = _login(client, "bob")

    # Alice crée un projet et invite Bob
    r = client.post(
        "/api/projects/",
        json.dumps({"title": "P1", "description": "", "type": "BACK_END"}),
        content_type="application/json",
        **alice_auth,
    )
    p_id = r.json()["id"]
    client.post(
        f"/api/projects/{p_id}/users/",
        json.dumps({"user": bob.id}),
        content_type="application/json",
        **alice_auth,
    )

    # Bob tente PATCH → 403 (contributeur mais pas auteur)
    r = client.patch(
        f"/api/projects/{p_id}/",
        json.dumps({"title": "Hack"}),
        content_type="application/json",
        **bob_auth,
    )
    assert r.status_code == 403


def test_project_create_makes_author_contributor(client, alice):
    """CDC métier : à la création d'un projet, l'auteur est automatiquement contributeur."""
    alice_auth = _login(client, "alice")

    r = client.post(
        "/api/projects/",
        json.dumps({"title": "P1", "description": "", "type": "BACK_END"}),
        content_type="application/json",
        **alice_auth,
    )
    assert r.status_code == 201
    p_id = r.json()["id"]

    # Alice doit voir le projet dans sa liste (=> elle est contributrice)
    r = client.get("/api/projects/", **alice_auth)
    assert r.json()["count"] == 1
    assert r.json()["results"][0]["id"] == p_id
