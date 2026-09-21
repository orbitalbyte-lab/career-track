from collections.abc import Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.database.connection import SessionLocal
from app.database.models.user import UserDB
from app.security.jwt import decode_access_token


security = HTTPBearer(auto_error=False)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
    db: Session = Depends(get_db),
) -> UserDB:
    authentication_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if credentials is None:
        raise authentication_error

    payload = decode_access_token(credentials.credentials)

    if payload is None:
        raise authentication_error

    subject = payload.get("sub")

    if not isinstance(subject, str):
        raise authentication_error

    try:
        user_id = int(subject)
    except ValueError:
        raise authentication_error from None

    user = (
        db.query(UserDB)
        .filter(UserDB.id == user_id)
        .first()
    )

    if user is None or not user.is_active:
        raise authentication_error

    return user