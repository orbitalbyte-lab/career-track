from sqlalchemy.orm import Session

from app.database.models.follow_up import FollowUpDB
from app.models.follow_up import FollowUp
from app.repositories.follow_up_repository import (
    FollowUpRepository,
)
from app.repositories.application_repository import (
    ApplicationRepository,
)

class FollowUpService:
    def __init__(self, session: Session) -> None:
        self.repository = FollowUpRepository(session)
        self.application_repository = ApplicationRepository(session)

    def create_follow_up(
        self,
        follow_up: FollowUp,
        user_id: int | None = None,
    ) -> FollowUpDB:
        if user_id is not None:
            application = self.application_repository.get_by_id(
                application_id=follow_up.application_id,
                user_id=user_id,
            )

            if application is None:
                raise ValueError("Application not found.")

        return self.repository.create(follow_up)

    def get_follow_ups(
        self,
        offset: int = 0,
        limit: int | None = None,
        user_id: int | None = None,
    ) -> list[FollowUpDB]:
        return self.repository.get_all(
            offset=offset,
            limit=limit,
            user_id=user_id,
        )

    def get_follow_up(
        self,
        follow_up_id: int,
        user_id: int | None = None,
    ) -> FollowUpDB | None:
        return self.repository.get_by_id(
            follow_up_id=follow_up_id,
            user_id=user_id,
        )

    def complete_follow_up(
        self,
        follow_up_id: int,
        user_id: int | None = None,
    ) -> FollowUpDB | None:
        return self.repository.update(
            follow_up_id=follow_up_id,
            completed=True,
            user_id=user_id,
        )

    def reopen_follow_up(
        self,
        follow_up_id: int,
        user_id: int | None = None,
    ) -> FollowUpDB | None:
        return self.repository.update(
            follow_up_id=follow_up_id,
            completed=False,
            user_id=user_id,
        )
    def delete_follow_up(
        self,
        follow_up_id: int,
        user_id: int | None = None,
    ) -> bool:
        return self.repository.delete(
            follow_up_id=follow_up_id,
            user_id=user_id,
        )
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
            "completed": sum(1 for follow_up in follow_ups if follow_up.completed),
            "pending": sum(1 for follow_up in follow_ups if not follow_up.completed),
        }
