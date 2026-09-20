from sqlalchemy.orm import Session

from app.database.models.user import UserDB
from app.repositories.user_repository import UserRepository
from app.security.jwt import create_access_token
from app.security.passwords import hash_password, verify_password


class AuthService:
    def __init__(self, session: Session) -> None:
        self.user_repository = UserRepository(session)

    def register_user(
        self,
        email: str,
        password: str,
    ) -> UserDB:
        existing_user = self.user_repository.get_by_email(email)

        if existing_user is not None:
            raise ValueError("Email is already registered.")

        user = UserDB(
            email=email,
            password_hash=hash_password(password),
            is_active=True,
        )

        return self.user_repository.create(user)

    def authenticate_user(
        self,
        email: str,
        password: str,
    ) -> UserDB | None:
        normalized_email = email.strip().lower()

        user = self.user_repository.get_by_email(
            normalized_email
        )

        if user is None:
            return None

        if not user.is_active:
            return None

        if not verify_password(
            password,
            user.password_hash,
        ):
            return None

        return user

    def login_user(
        self,
        email: str,
        password: str,
    ) -> str | None:
        user = self.authenticate_user(
            email=email,
            password=password,
        )

        if user is None:
            return None

        return create_access_token(str(user.id))