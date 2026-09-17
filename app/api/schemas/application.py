from datetime import date
from urllib.parse import urlparse

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from app.models.application import ApplicationStatus, ApplicationType


class ApplicationBase(BaseModel):
    company_id: int = Field(gt=0)
    position: str = Field(min_length=1, max_length=200)
    application_type: ApplicationType
    date_applied: date
    status: ApplicationStatus = ApplicationStatus.WISHLIST
    location: str | None = Field(default=None, max_length=200)
    deadline: date | None = None
    job_url: str | None = Field(default=None, max_length=500)
    notes: str | None = Field(default=None, max_length=2000)

    @field_validator("position")
    @classmethod
    def validate_position(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Position cannot be empty.")

        return value

    @field_validator("date_applied")
    @classmethod
    def validate_date_applied(cls, value: date) -> date:
        if value > date.today():
            raise ValueError("Application date cannot be in the future.")

        return value

    @field_validator("job_url")
    @classmethod
    def validate_job_url(cls, value: str | None) -> str | None:
        if value is None:
            return None

        value = value.strip()

        if not value:
            return None

        parsed = urlparse(value)

        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            raise ValueError("Job URL must be a valid HTTP or HTTPS URL.")

        return value

    @model_validator(mode="after")
    def validate_deadline_after_application_date(self):
        if (
            self.deadline is not None
            and self.deadline < self.date_applied
        ):
            raise ValueError(
                "Deadline cannot be before the application date."
            )

        return self


class ApplicationCreate(ApplicationBase):
    pass


class ApplicationUpdate(BaseModel):
    position: str | None = Field(
        default=None,
        min_length=1,
        max_length=200,
    )
    application_type: ApplicationType | None = None
    date_applied: date | None = None
    status: ApplicationStatus | None = None
    location: str | None = Field(default=None, max_length=200)
    deadline: date | None = Field(default=None)
    job_url: str | None = Field(default=None, max_length=500)
    notes: str | None = Field(default=None, max_length=2000)

    @field_validator("position")
    @classmethod
    def validate_position(cls, value: str | None) -> str | None:
        if value is None:
            return None

        value = value.strip()

        if not value:
            raise ValueError("Position cannot be empty.")

        return value

    @field_validator("date_applied")
    @classmethod
    def validate_date_applied(
        cls,
        value: date | None,
    ) -> date | None:
        if value is not None and value > date.today():
            raise ValueError("Application date cannot be in the future.")

        return value

    @field_validator("job_url")
    @classmethod
    def validate_job_url(cls, value: str | None) -> str | None:
        if value is None:
            return None

        value = value.strip()

        if not value:
            return None

        parsed = urlparse(value)

        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            raise ValueError("Job URL must be a valid HTTP or HTTPS URL.")

        return value


class ApplicationResponse(ApplicationBase):
    model_config = ConfigDict(from_attributes=True)

    id: int