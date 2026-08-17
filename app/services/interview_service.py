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

    def get_interview(
        self,
        interview_id,
    ):
        return (
            self.repository.get_by_id(
                interview_id
            )
        )    

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
    def get_upcoming_interviews(
        self,
    ):
        return (
            self.repository.get_upcoming()
        )     
    def search_interviews(
        self,
        query,
    ):
        return (
            self.repository.search(
                query
            )
        )    
    def get_interviews_by_status(
        self,
        status,
    ):
        return (
            self.repository.get_by_status(
                status
            )
        )       