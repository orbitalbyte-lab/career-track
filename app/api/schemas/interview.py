from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.models.interview import (
    InterviewOutcome,
    InterviewStatus,
    InterviewType,
)


class InterviewBase(BaseModel):
    application_id: int = Field(gt=0)
    scheduled_at: datetime
    interview_type: InterviewType
    status: InterviewStatus = InterviewStatus.SCHEDULED
    outcome: InterviewOutcome = InterviewOutcome.PENDING
    notes: str | None = Field(default=None, max_length=2000)

    @field_validator("scheduled_at")
    @classmethod
    def validate_scheduled_at(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("Scheduled time must include a timezone.")

        return value


class InterviewCreate(InterviewBase):
    pass


class InterviewUpdate(BaseModel):
    status: InterviewStatus
    outcome: InterviewOutcome | None = None


class InterviewResponse(InterviewBase):
    model_config = ConfigDict(from_attributes=True)

    id: int