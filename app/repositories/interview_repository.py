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
        return (
        self.session.query(
            InterviewDB
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
    