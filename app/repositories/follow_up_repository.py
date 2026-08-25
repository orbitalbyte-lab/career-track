from datetime import datetime

from app.database.models.follow_up import (
    FollowUpDB,
)


class FollowUpRepository:
    def __init__(self, session):
        self.session = session

    def create(self, follow_up):
        follow_up_db = FollowUpDB(
            application_id=follow_up.application_id,
            follow_up_at=follow_up.follow_up_at,
            note=follow_up.note,
            completed=follow_up.completed,
        )

        self.session.add(follow_up_db)
        self.session.commit()

        return follow_up_db

    def get_all(self):
        return (
            self.session.query(
                FollowUpDB
            )
            .order_by(
                FollowUpDB.follow_up_at
            )
            .all()
        )

    def get_by_id(
        self,
        follow_up_id,
    ):
        return (
            self.session.query(
                FollowUpDB
            )
            .filter_by(
                id=follow_up_id
            )
            .first()
        )

    def update(
        self,
        follow_up_id,
        completed,
    ):
        follow_up = self.get_by_id(
            follow_up_id
        )

        if follow_up is None:
            return None

        follow_up.completed = completed

        self.session.commit()

        return follow_up

    def delete(
        self,
        follow_up_id,
    ):
        follow_up = self.get_by_id(
            follow_up_id
        )

        if follow_up is None:
            return False

        self.session.delete(
            follow_up
        )

        self.session.commit()

        return True

    def get_upcoming(self):
        return (
            self.session.query(
                FollowUpDB
            )
            .filter(
                FollowUpDB.follow_up_at
                >= datetime.now(),
                FollowUpDB.completed.is_(False),
            )
            .order_by(
                FollowUpDB.follow_up_at
            )
            .all()
        )

    def get_pending(self):
        return (
            self.session.query(
                FollowUpDB
            )
            .filter_by(
                completed=False
            )
            .order_by(
                FollowUpDB.follow_up_at
            )
            .all()
        )

    def get_completed(self):
        return (
            self.session.query(
                FollowUpDB
            )
            .filter_by(
                completed=True
            )
            .order_by(
                FollowUpDB.follow_up_at
            )
            .all()
        )