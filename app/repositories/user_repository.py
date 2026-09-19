from sqlalchemy.orm import Session

from app.database.models.user import UserDB


class UserRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, user: UserDB) -> UserDB:
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)

        return user

    def get_by_email(self, email: str) -> UserDB | None:
        return (
            self.session.query(UserDB)
            .filter(UserDB.email == email)
            .first()
        )

    def get_by_id(self, user_id: int) -> UserDB | None:
        return (
            self.session.query(UserDB)
            .filter(UserDB.id == user_id)
            .first()
        )