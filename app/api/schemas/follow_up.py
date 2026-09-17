from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

class FollowUpBase(BaseModel):
    application_id: int = Field(gt=0)
    follow_up_at: datetime
    note: str = Field(min_length=1, max_length=2000)
    completed: bool = False

    @field_validator("follow_up_at")
    @classmethod
    def validate_follow_up_at(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("Follow-up time must include a timezone.")

        return value

    @field_validator("note")
    @classmethod
    def validate_note(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Follow-up note cannot be empty.")

        return value


class FollowUpCreate(FollowUpBase):
    pass


class FollowUpUpdate(BaseModel):
    completed: bool


class FollowUpResponse(FollowUpBase):
    model_config = ConfigDict(from_attributes=True)

    id: int