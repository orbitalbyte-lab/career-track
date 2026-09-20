import pytest

from app.security.jwt import decode_access_token
from app.services.auth_service import AuthService
from app.security.passwords import verify_password


def test_auth_service_registers_user(db_session):
    service = AuthService(db_session)

    user = service.register_user(
        email="test@example.com",
        password="TestPassword123!",
    )

    assert user.id is not None
    assert user.email == "test@example.com"
    assert user.is_active is True


def test_auth_service_hashes_password(db_session):
    service = AuthService(db_session)

    user = service.register_user(
        email="test@example.com",
        password="TestPassword123!",
    )

    assert user.password_hash != "TestPassword123!"
    assert verify_password(
        "TestPassword123!",
        user.password_hash,
    )


def test_auth_service_rejects_duplicate_email(db_session):
    service = AuthService(db_session)

    service.register_user(
        email="test@example.com",
        password="TestPassword123!",
    )

    with pytest.raises(
        ValueError,
        match="Email is already registered",
    ):
        service.register_user(
            email="test@example.com",
            password="AnotherPassword123!",
        )


def test_auth_service_stores_normalized_email(db_session):
    service = AuthService(db_session)

    user = service.register_user(
        email="test@example.com",
        password="TestPassword123!",
    )

    assert user.email == "test@example.com"


def test_auth_service_authenticates_valid_credentials(
    db_session,
):
    service = AuthService(db_session)

    created_user = service.register_user(
        email="test@example.com",
        password="TestPassword123!",
    )

    authenticated_user = service.authenticate_user(
        email="test@example.com",
        password="TestPassword123!",
    )

    assert authenticated_user is not None
    assert authenticated_user.id == created_user.id
    assert authenticated_user.email == "test@example.com"


def test_auth_service_rejects_wrong_password(
    db_session,
):
    service = AuthService(db_session)

    service.register_user(
        email="test@example.com",
        password="TestPassword123!",
    )

    authenticated_user = service.authenticate_user(
        email="test@example.com",
        password="WrongPassword123!",
    )

    assert authenticated_user is None


def test_auth_service_rejects_unknown_email(
    db_session,
):
    service = AuthService(db_session)

    authenticated_user = service.authenticate_user(
        email="missing@example.com",
        password="TestPassword123!",
    )

    assert authenticated_user is None


def test_auth_service_rejects_inactive_user(
    db_session,
):
    service = AuthService(db_session)

    user = service.register_user(
        email="test@example.com",
        password="TestPassword123!",
    )

    user.is_active = False
    db_session.commit()

    authenticated_user = service.authenticate_user(
        email="test@example.com",
        password="TestPassword123!",
    )

    assert authenticated_user is None


def test_auth_service_normalizes_login_email(
    db_session,
):
    service = AuthService(db_session)

    service.register_user(
        email="test@example.com",
        password="TestPassword123!",
    )

    authenticated_user = service.authenticate_user(
        email="  TEST@EXAMPLE.COM  ",
        password="TestPassword123!",
    )

    assert authenticated_user is not None
    assert authenticated_user.email == "test@example.com"

def test_auth_service_login_returns_access_token(
    db_session,
    monkeypatch,
):
    monkeypatch.setenv(
        "JWT_SECRET_KEY",
        "test-secret-key-for-login-jwt-hs256-32-bytes-minimum",
    )

    service = AuthService(db_session)

    user = service.register_user(
        email="test@example.com",
        password="TestPassword123!",
    )

    token = service.login_user(
        email="test@example.com",
        password="TestPassword123!",
    )

    assert token is not None

    payload = decode_access_token(token)

    assert payload is not None
    assert payload["sub"] == str(user.id)


def test_auth_service_login_rejects_wrong_password(
    db_session,
    monkeypatch,
):
    monkeypatch.setenv(
        "JWT_SECRET_KEY",
        "test-secret-key-for-login-jwt-hs256-32-bytes-minimum",
    )

    service = AuthService(db_session)

    service.register_user(
        email="test@example.com",
        password="TestPassword123!",
    )

    token = service.login_user(
        email="test@example.com",
        password="WrongPassword123!",
    )

    assert token is None


def test_auth_service_login_rejects_unknown_email(
    db_session,
    monkeypatch,
):
    monkeypatch.setenv(
        "JWT_SECRET_KEY",
        "test-secret-key-for-login-jwt-hs256-32-bytes-minimum",
    )

    service = AuthService(db_session)

    token = service.login_user(
        email="missing@example.com",
        password="TestPassword123!",
    )

    assert token is None


def test_auth_service_login_rejects_inactive_user(
    db_session,
    monkeypatch,
):
    monkeypatch.setenv(
        "JWT_SECRET_KEY",
        "test-secret-key-for-login-jwt-hs256-32-bytes-minimum",
    )

    service = AuthService(db_session)

    user = service.register_user(
        email="test@example.com",
        password="TestPassword123!",
    )

    user.is_active = False
    db_session.commit()

    token = service.login_user(
        email="test@example.com",
        password="TestPassword123!",
    )

    assert token is None