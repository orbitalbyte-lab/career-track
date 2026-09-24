from datetime import timedelta

import pytest
import jwt
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials

from app.api.dependencies import get_current_user
from app.database.models.user import UserDB
from app.security.jwt import create_access_token


TEST_SECRET_KEY = (
    "test-secret-key-for-dependencies-hs256-with-32-bytes-minimum"
)


def test_get_current_user_returns_authenticated_user(
    db_session,
    monkeypatch,
):
    monkeypatch.setenv(
        "JWT_SECRET_KEY",
        TEST_SECRET_KEY,
    )

    user = UserDB(
        email="test@example.com",
        password_hash="test-hash",
        is_active=True,
    )

    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    token = create_access_token(str(user.id))

    credentials = HTTPAuthorizationCredentials(
        scheme="Bearer",
        credentials=token,
    )

    result = get_current_user(
        credentials=credentials,
        db=db_session,
    )

    assert result.id == user.id
    assert result.email == "test@example.com"


def test_get_current_user_rejects_missing_credentials(
    db_session,
):
    with pytest.raises(HTTPException) as exc_info:
        get_current_user(
            credentials=None,
            db=db_session,
        )

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Could not validate credentials."
    assert exc_info.value.headers["WWW-Authenticate"] == "Bearer"


def test_get_current_user_rejects_invalid_token(
    db_session,
    monkeypatch,
):
    monkeypatch.setenv(
        "JWT_SECRET_KEY",
        TEST_SECRET_KEY,
    )

    credentials = HTTPAuthorizationCredentials(
        scheme="Bearer",
        credentials="invalid-token",
    )

    with pytest.raises(HTTPException) as exc_info:
        get_current_user(
            credentials=credentials,
            db=db_session,
        )

    assert exc_info.value.status_code == 401


def test_get_current_user_rejects_unknown_user(
    db_session,
    monkeypatch,
):
    monkeypatch.setenv(
        "JWT_SECRET_KEY",
        TEST_SECRET_KEY,
    )

    token = create_access_token("999999")

    credentials = HTTPAuthorizationCredentials(
        scheme="Bearer",
        credentials=token,
    )

    with pytest.raises(HTTPException) as exc_info:
        get_current_user(
            credentials=credentials,
            db=db_session,
        )

    assert exc_info.value.status_code == 401


def test_get_current_user_rejects_inactive_user(
    db_session,
    monkeypatch,
):
    monkeypatch.setenv(
        "JWT_SECRET_KEY",
        TEST_SECRET_KEY,
    )

    user = UserDB(
        email="inactive@example.com",
        password_hash="test-hash",
        is_active=False,
    )

    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    token = create_access_token(str(user.id))

    credentials = HTTPAuthorizationCredentials(
        scheme="Bearer",
        credentials=token,
    )

    with pytest.raises(HTTPException) as exc_info:
        get_current_user(
            credentials=credentials,
            db=db_session,
        )

    assert exc_info.value.status_code == 401

def test_get_current_user_rejects_expired_token(
    db_session,
    monkeypatch,
):
    monkeypatch.setenv(
        "JWT_SECRET_KEY",
        TEST_SECRET_KEY,
    )

    token = create_access_token(
        "1",
        expires_delta=timedelta(seconds=-1),
    )

    credentials = HTTPAuthorizationCredentials(
        scheme="Bearer",
        credentials=token,
    )

    with pytest.raises(HTTPException) as exc_info:
        get_current_user(
            credentials=credentials,
            db=db_session,
        )

    assert exc_info.value.status_code == 401
    assert exc_info.value.headers["WWW-Authenticate"] == "Bearer"


def test_get_current_user_rejects_non_bearer_scheme(
    db_session,
    monkeypatch,
):
    monkeypatch.setenv(
        "JWT_SECRET_KEY",
        TEST_SECRET_KEY,
    )

    token = create_access_token("1")

    credentials = HTTPAuthorizationCredentials(
        scheme="Basic",
        credentials=token,
    )

    with pytest.raises(HTTPException) as exc_info:
        get_current_user(
            credentials=credentials,
            db=db_session,
        )

    assert exc_info.value.status_code == 401
    assert exc_info.value.headers["WWW-Authenticate"] == "Bearer"

def test_get_current_user_rejects_token_without_subject(
    db_session,
    monkeypatch,
):
    monkeypatch.setenv(
        "JWT_SECRET_KEY",
        TEST_SECRET_KEY,
    )

    token = jwt.encode(
        {},
        TEST_SECRET_KEY,
        algorithm="HS256",
    )

    credentials = HTTPAuthorizationCredentials(
        scheme="Bearer",
        credentials=token,
    )

    with pytest.raises(HTTPException) as exc_info:
        get_current_user(
            credentials=credentials,
            db=db_session,
        )

    assert exc_info.value.status_code == 401
    assert exc_info.value.headers["WWW-Authenticate"] == "Bearer"


def test_get_current_user_rejects_non_numeric_subject(
    db_session,
    monkeypatch,
):
    monkeypatch.setenv(
        "JWT_SECRET_KEY",
        TEST_SECRET_KEY,
    )

    token = jwt.encode(
        {"sub": "not-a-user-id"},
        TEST_SECRET_KEY,
        algorithm="HS256",
    )

    credentials = HTTPAuthorizationCredentials(
        scheme="Bearer",
        credentials=token,
    )

    with pytest.raises(HTTPException) as exc_info:
        get_current_user(
            credentials=credentials,
            db=db_session,
        )

    assert exc_info.value.status_code == 401
    assert exc_info.value.headers["WWW-Authenticate"] == "Bearer"