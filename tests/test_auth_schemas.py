import pytest
from pydantic import ValidationError

from app.api.schemas.auth import RegisterRequest, UserResponse


def test_register_request_normalizes_email():
    request = RegisterRequest(
        email="  Test@Example.COM  ",
        password="TestPassword123!",
    )

    assert request.email == "test@example.com"


def test_register_request_accepts_valid_password():
    request = RegisterRequest(
        email="test@example.com",
        password="TestPassword123!",
    )

    assert request.password == "TestPassword123!"


def test_register_request_rejects_short_password():
    with pytest.raises(ValidationError):
        RegisterRequest(
            email="test@example.com",
            password="short",
        )


def test_register_request_rejects_invalid_email():
    with pytest.raises(ValidationError):
        RegisterRequest(
            email="not-an-email",
            password="TestPassword123!",
        )


def test_user_response_does_not_expose_password_hash():
    response = UserResponse(
        id=1,
        email="test@example.com",
        is_active=True,
        created_at="2026-09-19T10:00:00",
        updated_at="2026-09-19T10:00:00",
    )

    data = response.model_dump()

    assert "password" not in data
    assert "password_hash" not in data
    assert data["email"] == "test@example.com"