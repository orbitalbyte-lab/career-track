from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class InterviewType(str, Enum):
    ONLINE = "Online"
    PHONE = "Phone"
    ONSITE = "On-site"


class InterviewStatus(str, Enum):
    SCHEDULED = "Scheduled"
    COMPLETED = "Completed"
    CANCELED = "Canceled"


@dataclass
class Interview:
    application_id: int
    scheduled_at: datetime
    interview_type: InterviewType
    status: InterviewStatus = (
        InterviewStatus.SCHEDULED
    )
    notes: str | None = None

    def __post_init__(self) -> None:
        if self.application_id <= 0:
            raise ValueError(
                "Invalid application ID."
            )

        if not isinstance(
            self.interview_type,
            InterviewType,
        ):
            raise ValueError(
                "Invalid interview type."
            )

        if not isinstance(
            self.status,
            InterviewStatus,
        ):
            raise ValueError(
                "Invalid interview status."
            )