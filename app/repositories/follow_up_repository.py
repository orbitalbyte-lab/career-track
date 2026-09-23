from datetime import UTC, datetime

from sqlalchemy.orm import Session

from app.database.models.application import ApplicationDB
from app.database.models.company import CompanyDB
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

    def get_all(
        self,
        offset: int = 0,
        limit: int | None = None,
        user_id: int | None = None,
    ) -> list[FollowUpDB]:
        query = self.session.query(FollowUpDB)

        if user_id is not None:
            query = (
                query
                .join(FollowUpDB.application)
                .join(ApplicationDB.company)
                .filter(CompanyDB.user_id == user_id)
            )

        query = query.order_by(FollowUpDB.follow_up_at)

        if offset > 0:
            query = query.offset(offset)

        if limit is not None:
            query = query.limit(limit)

        return query.all()
    def get_by_id(
        self,
        follow_up_id: int,
        user_id: int | None = None,
    ) -> FollowUpDB | None:
        query = self.session.query(FollowUpDB).filter(
            FollowUpDB.id == follow_up_id
        )

        if user_id is not None:
            query = (
                query
                .join(FollowUpDB.application)
                .join(ApplicationDB.company)
                .filter(CompanyDB.user_id == user_id)
            )

        return query.first()

    def update(
        self,
        follow_up_id: int,
        completed: bool,
        user_id: int | None = None,
    ) -> FollowUpDB | None:
        follow_up = self.get_by_id(
            follow_up_id=follow_up_id,
            user_id=user_id,
        )

        if follow_up is None:
            return None

        follow_up.completed = completed

        self.session.commit()
        self.session.refresh(follow_up)

        return follow_up

    def delete(
        self,
        follow_up_id: int,
        user_id: int | None = None,
    ) -> bool:
        follow_up = self.get_by_id(
            follow_up_id=follow_up_id,
            user_id=user_id,
        )

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
