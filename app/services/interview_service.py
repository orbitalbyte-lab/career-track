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
        outcome=None,
    ):
        return self.repository.update(
            interview_id,
            status,
            outcome,
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

    def get_interview_analytics(
        self,
    ):
        interviews = (
            self.get_interviews()
        )

        analytics = {
            "total": len(interviews),
            "completed": 0,
            "cancelled": 0,
            "online": 0,
            "phone": 0,
            "on_site": 0,
            "passed": 0,
            "failed": 0,
            "pending": 0,
        }

        for interview in interviews:
            status = (
                interview.status.lower()
            )

            interview_type = (
                interview.interview_type.lower()
            )

            outcome = (
                interview.outcome.lower()
            )

            if status == "completed":
                analytics[
                    "completed"
                ] += 1

            elif status in (
                "cancelled",
                "canceled",
            ):
                analytics[
                    "cancelled"
                ] += 1

            if interview_type == "online":
                analytics[
                    "online"
                ] += 1

            elif interview_type == "phone":
                analytics[
                    "phone"
                ] += 1

            elif interview_type in (
                "on-site",
                "on site",
            ):
                analytics[
                    "on_site"
                ] += 1

            if outcome == "passed":
                analytics[
                    "passed"
                ] += 1

            elif outcome == "failed":
                analytics[
                    "failed"
                ] += 1

            elif outcome == "pending":
                analytics[
                    "pending"
                ] += 1

        return analytics

    def get_this_week_interviews(
        self,
    ):
        return (
            self.repository.get_this_week()
        )

    def get_recent_interviews(
        self,
    ):
        return (
            self.repository
            .get_all_sorted_by_date()
        )