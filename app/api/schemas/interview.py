from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.interview import (
    InterviewOutcome,
    InterviewStatus,
    InterviewType,
)


class InterviewBase(BaseModel):
    application_id: int
    scheduled_at: datetime
    interview_type: InterviewType
    status: InterviewStatus = InterviewStatus.SCHEDULED
    outcome: InterviewOutcome = InterviewOutcome.PENDING
    notes: str | None = None


class InterviewCreate(InterviewBase):
    pass


class InterviewUpdate(BaseModel):
    status: InterviewStatus
    outcome: InterviewOutcome | None = None


class InterviewResponse(InterviewBase):
    model_config = ConfigDict(from_attributes=True)

    id: int