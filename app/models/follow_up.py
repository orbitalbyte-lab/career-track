from dataclasses import dataclass
from datetime import datetime


@dataclass
class FollowUp:
    application_id: int
    follow_up_at: datetime
    note: str
    completed: bool = False

    def __post_init__(self) -> None:
        if self.application_id <= 0:
            raise ValueError(
                "Invalid application ID."
            )

        if not isinstance(
            self.follow_up_at,
            datetime,
        ):
            raise ValueError(
                "Invalid follow-up date."
            )

        if not self.note.strip():
            raise ValueError(
                "Follow-up note cannot be empty."
            )

        if not isinstance(
            self.completed,
            bool,
        ):
            raise ValueError(
                "Invalid completion status."
            )