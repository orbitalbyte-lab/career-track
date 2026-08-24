from app.database.models.interview import (
    InterviewDB,
)


class InterviewRepository:
    def __init__(self, session):
        self.session = session

    def create(self, interview):
        interview_db = InterviewDB(
            application_id=interview.application_id,
            scheduled_at=interview.scheduled_at,
            interview_type=(
                interview.interview_type.value
            ),
            status=interview.status.value,
            outcome=interview.outcome.value,
            notes=interview.notes,
        )

        self.session.add(interview_db)
        self.session.commit()

        return interview_db

    def get_all(self):
        return (
            self.session.query(
                InterviewDB
            ).all()
        )

    def get_by_id(
        self,
        interview_id,
    ):
        return (
            self.session.query(
                InterviewDB
            )
            .filter_by(
                id=interview_id
            )
            .first()
        )

    def update(
        self,
        interview_id,
        status,
        outcome,
    ):
        interview = self.get_by_id(
            interview_id
        )

        if interview is None:
            return None

        interview.status = status
        interview.outcome = outcome

        self.session.commit()

        return interview

    def delete(
        self,
        interview_id,
    ):
        interview = self.get_by_id(
            interview_id
        )

        if interview is None:
            return False

        self.session.delete(
            interview
        )

        self.session.commit()

        return True

    def get_upcoming(
        self,
    ):
        from datetime import datetime

        return (
            self.session.query(
                InterviewDB
            )
            .filter(
                InterviewDB.scheduled_at
                >= datetime.now()
            )
            .order_by(
                InterviewDB.scheduled_at
           )
            .all()
        )
    def get_by_status(
        self,
        status,
    ):
        return (
            self.session.query(
                InterviewDB
            )
            .filter_by(
                status=status
            )
            .all()
        )

    def search(
        self,
        query,
    ):
        return (
            self.session.query(
                InterviewDB
            )
            .filter(
                InterviewDB.status.ilike(
                    f"%{query}%"
                )
                |
                InterviewDB.interview_type.ilike(
                    f"%{query}%"
                )
            )
            .all()
        )

    def get_this_week(
        self,
    ):
        from datetime import datetime, timedelta

        now = datetime.now()

        start_of_week = now - timedelta(
            days=now.weekday()
        )

        start_of_week = start_of_week.replace(
            hour=0,
            minute=0,
            second=0,
            microsecond=0,
        )

        end_of_week = (
            start_of_week
            + timedelta(days=7)
        )

        return (
            self.session.query(
                InterviewDB
            )
            .filter(
                InterviewDB.scheduled_at
                >= start_of_week,
                InterviewDB.scheduled_at
                < end_of_week,
            )
            .order_by(
                InterviewDB.scheduled_at
            )
            .all()
        )
    def get_all_sorted_by_date(
        self,
    ):
        return (
            self.session.query(
                InterviewDB
            )
            .order_by(
                InterviewDB.scheduled_at.desc()
            )
            .all()
        )

    def get_all_sorted(
        self,
        field: str,
    ):
        query = self.session.query(
            InterviewDB
        )

        if field == "date":
            return (
                query
                .order_by(
                    InterviewDB.scheduled_at.desc()
                )
                .all()
            )

        if field == "type":
            return (
                query
                .order_by(
                    InterviewDB.interview_type.asc()
                )
                .all()
            )

        return query.all()