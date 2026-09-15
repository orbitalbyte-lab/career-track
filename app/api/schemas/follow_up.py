from datetime import datetime

from pydantic import BaseModel, ConfigDict

class FollowUpBase(BaseModel):
    application_id: int
    follow_up_at: datetime
    note: str
    completed: bool = False


class FollowUpCreate(FollowUpBase):
    pass


class FollowUpUpdate(BaseModel):
    completed: bool


class FollowUpResponse(FollowUpBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
