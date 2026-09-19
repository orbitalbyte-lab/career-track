import pytest
from fastapi.testclient import TestClient

from app.api.dependencies import get_db
from app.api.main import app
from app.database.models.user import UserDB
from app.security.passwords import verify_password


def get_client(db_session):
    app.dependency_overrides[get_db] = lambda: db_session
    return TestClient(app)


def test_register_user(db_session):
    client = get_client(db_session)

    response = client.post(
        "/api/auth/register",
        json={
            "email": "Test@Example.COM",
            "password": "TestPassword123!",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["id"] == 1
    assert data["email"] == "test@example.com"
    assert data["is_active"] is True
    assert "password" not in data
    assert "password_hash" not in data


def test_register_user_stores_hashed_password(db_session):
    client = get_client(db_session)

    response = client.post(
        "/api/auth/register",
        json={
            "email": "test@example.com",
            "password": "TestPassword123!",
        },
    )

    assert response.status_code == 201

    user = db_session.query(UserDB).first()

    assert user is not None
    assert user.password_hash != "TestPassword123!"
    assert verify_password(
        "TestPassword123!",
        user.password_hash,
    )


def test_register_user_rejects_duplicate_email(db_session):
    client = get_client(db_session)

    payload = {
        "email": "test@example.com",
        "password": "TestPassword123!",
    }

    first_response = client.post(
        "/api/auth/register",
        json=payload,
    )

    second_response = client.post(
        "/api/auth/register",
        json={
            "email": "TEST@example.com",
            "password": "AnotherPassword123!",
        },
    )

    assert first_response.status_code == 201
    assert second_response.status_code == 409
    assert second_response.json() == {
        "detail": "Email is already registered."
    }


def test_register_user_rejects_short_password(db_session):
    client = get_client(db_session)

    response = client.post(
        "/api/auth/register",
        json={
            "email": "test@example.com",
            "password": "short",
        },
    )

    assert response.status_code == 422


def test_register_user_rejects_invalid_email(db_session):
    client = get_client(db_session)

    response = client.post(
        "/api/auth/register",
        json={
            "email": "not-an-email",
            "password": "TestPassword123!",
        },
    )

    assert response.status_code == 422


@pytest.fixture(autouse=True)
def clear_dependency_overrides():
    yield
    app.dependency_overrides.clear()