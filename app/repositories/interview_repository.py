from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.database.models.interview import InterviewDB
from app.models.interview import Interview


class InterviewRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create(
        self,
        interview: Interview,
    ) -> InterviewDB:
        interview_db = InterviewDB(
            application_id=interview.application_id,
            scheduled_at=interview.scheduled_at,
            interview_type=interview.interview_type.value,
            status=interview.status.value,
            outcome=interview.outcome.value,
            notes=interview.notes,
        )

        self.session.add(interview_db)
        self.session.commit()

        return interview_db

    def get_all(self) -> list[InterviewDB]:
        return self.session.query(InterviewDB).all()

    def get_by_id(
        self,
        interview_id: int,
    ) -> InterviewDB | None:
        return (
            self.session.query(InterviewDB)
            .filter_by(id=interview_id)
            .first()
        )

    def update(
        self,
        interview_id: int,
        status: str,
        outcome: str | None,
    ) -> InterviewDB | None:
        interview = self.get_by_id(interview_id)

        if interview is None:
            return None

        interview.status = status
        interview.outcome = outcome

        self.session.commit()

        return interview

    def delete(
        self,
        interview_id: int,
    ) -> bool:
        interview = self.get_by_id(interview_id)

        if interview is None:
            return False

        self.session.delete(interview)
        self.session.commit()

        return True

    def get_upcoming(self) -> list[InterviewDB]:
        return (
            self.session.query(InterviewDB)
            .filter(
                InterviewDB.scheduled_at >= datetime.now()
            )
            .order_by(InterviewDB.scheduled_at)
            .all()
        )

    def get_by_status(
        self,
        status: str,
    ) -> list[InterviewDB]:
        return (
            self.session.query(InterviewDB)
            .filter_by(status=status)
            .all()
        )

    def search(
        self,
        query: str,
    ) -> list[InterviewDB]:
        return (
            self.session.query(InterviewDB)
            .filter(
                InterviewDB.status.ilike(f"%{query}%")
                | InterviewDB.interview_type.ilike(
                    f"%{query}%"
                )
            )
            .all()
        )

    def get_this_week(self) -> list[InterviewDB]:
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

        end_of_week = start_of_week + timedelta(days=7)

        return (
            self.session.query(InterviewDB)
            .filter(
                InterviewDB.scheduled_at >= start_of_week,
                InterviewDB.scheduled_at < end_of_week,
            )
            .order_by(InterviewDB.scheduled_at)
            .all()
        )

    def get_all_sorted_by_date(
        self,
    ) -> list[InterviewDB]:
        return (
            self.session.query(InterviewDB)
            .order_by(
                InterviewDB.scheduled_at.desc()
            )
            .all()
        )

    def get_all_sorted(
        self,
        field: str,
    ) -> list[InterviewDB]:
        query = self.session.query(InterviewDB)

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