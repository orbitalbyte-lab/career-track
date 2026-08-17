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

    def delete_interview(
        self,
        interview_id,
    ):
        return self.repository.delete(
            interview_id
        )
    def get_interview_statistics(
        self,
    ):
        interviews = (
            self.get_interviews()
        )

        statistics = {}

        for interview in interviews:
            status = (
                interview.status
            )

            statistics[status] = (
                statistics.get(
                    status,
                    0,
                )
                + 1
            )

        return statistics    
    def search_interviews(
        self,
        query,
    ):
        return (
            self.repository.search(
                query
            )
        )       