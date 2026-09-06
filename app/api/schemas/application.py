from datetime import date

from pydantic import BaseModel, ConfigDict

from app.models.application import ApplicationStatus, ApplicationType


class ApplicationBase(BaseModel):
    company_id: int
    position: str
    application_type: ApplicationType
    date_applied: date
    status: ApplicationStatus = ApplicationStatus.WISHLIST
    location: str | None = None
    deadline: date | None = None
    job_url: str | None = None
    notes: str | None = None


class ApplicationCreate(ApplicationBase):
    pass


class ApplicationUpdate(BaseModel):
    position: str | None = None
    application_type: ApplicationType | None = None
    date_applied: date | None = None
    status: ApplicationStatus | None = None
    location: str | None = None
    deadline: date | None = None
    job_url: str | None = None
    notes: str | None = None


class ApplicationResponse(ApplicationBase):
    model_config = ConfigDict(from_attributes=True)

    id: int