from sqlalchemy.orm import Session

from app.database.models.user import UserDB
from app.repositories.user_repository import UserRepository
from app.security.passwords import hash_password


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