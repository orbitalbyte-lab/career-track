import os
from datetime import UTC, datetime, timedelta

import jwt
from jwt.exceptions import InvalidTokenError


ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def _get_secret_key() -> str:
    secret_key = os.getenv("JWT_SECRET_KEY")

    if not secret_key:
        raise RuntimeError(
            "JWT_SECRET_KEY environment variable is not set."
        )

    return secret_key


def create_access_token(
    subject: str,
    expires_delta: timedelta | None = None,
) -> str:
    now = datetime.now(UTC)

    if expires_delta is None:
        expires_delta = timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )

    expire = now + expires_delta

    payload = {
        "sub": subject,
        "iat": now,
        "exp": expire,
    }

    return jwt.encode(
        payload,
        _get_secret_key(),
        algorithm=ALGORITHM,
    )


def decode_access_token(
    token: str,
) -> dict[str, object] | None:
    try:
        return jwt.decode(
            token,
            _get_secret_key(),
            algorithms=[ALGORITHM],
        )
    except InvalidTokenError:
        return None