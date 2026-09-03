from datetime import UTC, datetime

from sqlalchemy.orm import Session

from app.database.models.follow_up import FollowUpDB
from app.models.follow_up import FollowUp


class FollowUpRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create(
        self,
        follow_up: FollowUp,
    ) -> FollowUpDB:
        follow_up_db = FollowUpDB(
            application_id=follow_up.application_id,
            follow_up_at=follow_up.follow_up_at,
            note=follow_up.note,
            completed=follow_up.completed,
        )

        self.session.add(follow_up_db)
        self.session.commit()
        self.session.refresh(follow_up_db)

        return follow_up_db

    def get_all(self) -> list[FollowUpDB]:
        return self.session.query(FollowUpDB).order_by(FollowUpDB.follow_up_at).all()

    def get_by_id(
        self,
        follow_up_id: int,
    ) -> FollowUpDB | None:
        return self.session.query(FollowUpDB).filter_by(id=follow_up_id).first()

    def update(
        self,
        follow_up_id: int,
        completed: bool,
    ) -> FollowUpDB | None:
        follow_up = self.get_by_id(follow_up_id)

        if follow_up is None:
            return None

        follow_up.completed = completed
        self.session.commit()
        self.session.refresh(follow_up)

        return follow_up

    def delete(
        self,
        follow_up_id: int,
    ) -> bool:
        follow_up = self.get_by_id(follow_up_id)

        if follow_up is None:
            return False

        self.session.delete(follow_up)
        self.session.commit()

        return True

    def get_upcoming(self) -> list[FollowUpDB]:
        return (
            self.session.query(FollowUpDB)
            .filter(
                FollowUpDB.follow_up_at >= datetime.now(UTC),
                FollowUpDB.completed.is_(False),
            )
            .order_by(FollowUpDB.follow_up_at)
            .all()
        )

    def get_pending(self) -> list[FollowUpDB]:
        return (
            self.session.query(FollowUpDB)
            .filter_by(completed=False)
            .order_by(FollowUpDB.follow_up_at)
            .all()
        )

    def get_completed(self) -> list[FollowUpDB]:
        return (
            self.session.query(FollowUpDB)
            .filter_by(completed=True)
            .order_by(FollowUpDB.follow_up_at)
            .all()
        )
