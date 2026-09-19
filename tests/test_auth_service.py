import pytest

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