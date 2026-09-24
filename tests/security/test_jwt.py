from datetime import timedelta

import jwt
import pytest

from app.security.jwt import create_access_token, decode_access_token


TEST_SECRET_KEY = "test-secret-key-for-jwt-" * 3


def test_create_and_decode_access_token(monkeypatch):
    monkeypatch.setenv("JWT_SECRET_KEY", TEST_SECRET_KEY)

    token = create_access_token("42")

    payload = decode_access_token(token)

    assert payload is not None
    assert payload["sub"] == "42"


def test_decode_access_token_rejects_expired_token(monkeypatch):
    monkeypatch.setenv("JWT_SECRET_KEY", TEST_SECRET_KEY)

    token = create_access_token(
        "42",
        expires_delta=timedelta(seconds=-1),
    )

    assert decode_access_token(token) is None


def test_decode_access_token_rejects_tampered_token(monkeypatch):
    monkeypatch.setenv("JWT_SECRET_KEY", TEST_SECRET_KEY)

    token = create_access_token("42")
    tampered_token = f"{token[:-1]}x"

    assert decode_access_token(tampered_token) is None


def test_decode_access_token_rejects_wrong_algorithm(monkeypatch):
    monkeypatch.setenv("JWT_SECRET_KEY", TEST_SECRET_KEY)

    token = jwt.encode(
        {"sub": "42"},
        TEST_SECRET_KEY,
        algorithm="HS512",
    )

    assert decode_access_token(token) is None


def test_create_access_token_requires_secret_key(monkeypatch):
    monkeypatch.delenv("JWT_SECRET_KEY", raising=False)

    with pytest.raises(RuntimeError, match="JWT_SECRET_KEY"):
        create_access_token("42")


def test_decode_access_token_requires_secret_key(monkeypatch):
    monkeypatch.delenv("JWT_SECRET_KEY", raising=False)

    with pytest.raises(RuntimeError, match="JWT_SECRET_KEY"):
        decode_access_token("invalid-token")
