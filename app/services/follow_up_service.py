from sqlalchemy.orm import Session

from app.database.models.follow_up import FollowUpDB
from app.models.follow_up import FollowUp
from app.repositories.follow_up_repository import (
    FollowUpRepository,
)


class FollowUpService:
    def __init__(self, session: Session) -> None:
        self.repository = FollowUpRepository(session)

    def create_follow_up(
        self,
        follow_up: FollowUp,
    ) -> FollowUpDB:
        return self.repository.create(follow_up)

    def get_follow_ups(self) -> list[FollowUpDB]:
        return self.repository.get_all()

    def get_follow_up(
        self,
        follow_up_id: int,
    ) -> FollowUpDB | None:
        return self.repository.get_by_id(follow_up_id)

    def complete_follow_up(
        self,
        follow_up_id: int,
    ) -> FollowUpDB | None:
        return self.repository.update(
            follow_up_id,
            True,
        )

    def reopen_follow_up(
        self,
        follow_up_id: int,
    ) -> FollowUpDB | None:
        return self.repository.update(
            follow_up_id,
            False,
        )

    def delete_follow_up(
        self,
        follow_up_id: int,
    ) -> bool:
        return self.repository.delete(follow_up_id)

    def get_upcoming_follow_ups(
        self,
    ) -> list[FollowUpDB]:
        return self.repository.get_upcoming()

    def get_pending_follow_ups(
        self,
    ) -> list[FollowUpDB]:
        return self.repository.get_pending()

    def get_completed_follow_ups(
        self,
    ) -> list[FollowUpDB]:
        return self.repository.get_completed()

    def get_follow_up_statistics(
        self,
    ) -> dict[str, int]:
        follow_ups = self.get_follow_ups()

        return {
            "total": len(follow_ups),
            "completed": sum(
                1
                for follow_up in follow_ups
                if follow_up.completed
            ),
            "pending": sum(
                1
                for follow_up in follow_ups
                if not follow_up.completed
            ),
        }