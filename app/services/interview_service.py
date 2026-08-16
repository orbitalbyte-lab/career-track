from app.repositories.interview_repository import (
    InterviewRepository,
)


class InterviewService:
    def __init__(self, session):
        self.repository = (
            InterviewRepository(session)
        )

    def create_interview(
        self,
        interview,
    ):
        return self.repository.create(
            interview
        )

    def get_interviews(self):
        return self.repository.get_all()

    def update_interview(
        self,
        interview_id,
        status,
    ):
        return self.repository.update(
            interview_id,
            status,
        )