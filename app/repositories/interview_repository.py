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
    ):
        interview = self.get_by_id(
            interview_id
        )

        if interview is None:
            return None

        interview.status = status

        self.session.commit()

        return interview    