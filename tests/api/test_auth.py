import pytest
from fastapi.testclient import TestClient

from app.api.dependencies import get_db
from app.api.main import app
from app.database.models.user import UserDB
from app.security.jwt import decode_access_token
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

    user = (
        db_session.query(UserDB)
        .filter(UserDB.email == "test@example.com")
        .first()
    )

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

def test_register_user_rejects_malformed_email(db_session):
    client = get_client(db_session)

    response = client.post(
        "/api/auth/register",
        json={
            "email": "user@.com",
            "password": "TestPassword123!",
        },
    )

    assert response.status_code == 422


def test_register_user_rejects_double_at_email(db_session):
    client = get_client(db_session)

    response = client.post(
        "/api/auth/register",
        json={
            "email": "user@@example.com",
            "password": "TestPassword123!",
        },
    )

    assert response.status_code == 422

def test_login_user_returns_access_token(
    db_session,
    monkeypatch,
):
    monkeypatch.setenv(
        "JWT_SECRET_KEY",
        "test-secret-key-for-api-login-hs256-with-32-bytes-minimum",
    )

    client = get_client(db_session)

    register_response = client.post(
        "/api/auth/register",
        json={
            "email": "test@example.com",
            "password": "TestPassword123!",
        },
    )

    assert register_response.status_code == 201

    user_id = register_response.json()["id"]

    response = client.post(
        "/api/auth/login",
        json={
            "email": "test@example.com",
            "password": "TestPassword123!",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["access_token"]
    assert data["token_type"] == "bearer"

    payload = decode_access_token(data["access_token"])

    assert payload is not None
    assert payload["sub"] == str(user_id)


def test_login_user_rejects_wrong_password(
    db_session,
    monkeypatch,
):
    monkeypatch.setenv(
        "JWT_SECRET_KEY",
        "test-secret-key-for-api-login-hs256-with-32-bytes-minimum",
    )

    client = get_client(db_session)

    register_response = client.post(
        "/api/auth/register",
        json={
            "email": "test@example.com",
            "password": "TestPassword123!",
        },
    )

    assert register_response.status_code == 201

    response = client.post(
        "/api/auth/login",
        json={
            "email": "test@example.com",
            "password": "WrongPassword123!",
        },
    )

    assert response.status_code == 401
    assert response.headers["WWW-Authenticate"] == "Bearer"
    assert response.json() == {
        "detail": "Invalid email or password.",
    }


def test_login_user_rejects_unknown_email(
    db_session,
    monkeypatch,
):
    monkeypatch.setenv(
        "JWT_SECRET_KEY",
        "test-secret-key-for-api-login-hs256-with-32-bytes-minimum",
    )

    client = get_client(db_session)

    response = client.post(
        "/api/auth/login",
        json={
            "email": "unknown@example.com",
            "password": "TestPassword123!",
        },
    )

    assert response.status_code == 401
    assert response.headers["WWW-Authenticate"] == "Bearer"
    assert response.json() == {
        "detail": "Invalid email or password.",
    }


def test_login_user_rejects_inactive_user(
    db_session,
    monkeypatch,
):
    monkeypatch.setenv(
        "JWT_SECRET_KEY",
        "test-secret-key-for-api-login-hs256-with-32-bytes-minimum",
    )

    client = get_client(db_session)

    register_response = client.post(
        "/api/auth/register",
        json={
            "email": "inactive@example.com",
            "password": "TestPassword123!",
        },
    )

    assert register_response.status_code == 201

    user = (
        db_session.query(UserDB)
        .filter(UserDB.email == "inactive@example.com")
        .first()
    )
    assert user is not None

    user.is_active = False
    db_session.commit()

    response = client.post(
        "/api/auth/login",
        json={
            "email": "inactive@example.com",
            "password": "TestPassword123!",
        },
    )

    assert response.status_code == 401
    assert response.headers["WWW-Authenticate"] == "Bearer"
    assert response.json() == {
        "detail": "Invalid email or password.",
    }
@pytest.fixture(autouse=True)
def clear_dependency_overrides():
    yield
    app.dependency_overrides.clear()

def test_get_current_user_profile(
    db_session,
    monkeypatch,
):
    monkeypatch.setenv(
        "JWT_SECRET_KEY",
        "test-secret-key-for-api-me-hs256-with-32-bytes-minimum",
    )

    client = get_client(db_session)

    register_response = client.post(
        "/api/auth/register",
        json={
            "email": "me@example.com",
            "password": "TestPassword123!",
        },
    )

    assert register_response.status_code == 201

    login_response = client.post(
        "/api/auth/login",
        json={
            "email": "me@example.com",
            "password": "TestPassword123!",
        },
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    client.headers.update(
        {
            "Authorization": f"Bearer {token}",
        }
    )

    response = client.get("/api/auth/me")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == register_response.json()["id"]
    assert data["email"] == "me@example.com"
    assert data["is_active"] is True
    assert "password" not in data
    assert "password_hash" not in data


def test_get_current_user_profile_requires_authentication(
    db_session,
):
    client = get_client(db_session)

    client.headers.pop("Authorization", None)

    response = client.get("/api/auth/me")

    assert response.status_code == 401
    assert response.headers["WWW-Authenticate"] == "Bearer"
    assert response.json() == {
        "detail": "Could not validate credentials."
    }
def test_login_user_rejects_short_password(db_session):
    client = get_client(db_session)

    response = client.post(
        "/api/auth/login",
        json={
            "email": "test@example.com",
            "password": "short",
        },
    )

    assert response.status_code == 422


def test_login_user_rejects_empty_email(db_session):
    client = get_client(db_session)

    response = client.post(
        "/api/auth/login",
        json={
            "email": "",
            "password": "TestPassword123!",
        },
    )

    assert response.status_code == 422
