from dataclasses import dataclass
from datetime import date
from enum import Enum

from app.models.company import Company


class ApplicationStatus(str, Enum):
    WISHLIST = "Wishlist"
    APPLIED = "Applied"
    UNDER_REVIEW = "Under Review"
    INTERVIEW = "Interview"
    OFFER = "Offer"
    REJECTED = "Rejected"
    WITHDRAWN = "Withdrawn"


class ApplicationType(str, Enum):
    INTERNSHIP = "Internship"
    FULL_TIME = "Full-time"
    PART_TIME = "Part-time"
    CONTRACT = "Contract"
    FREELANCE = "Freelance"


@dataclass
class Application:
    company: Company
    position: str
    application_type: ApplicationType
    date_applied: date
    status: ApplicationStatus = ApplicationStatus.WISHLIST
    location: str | None = None
    deadline: date | None = None
    job_url: str | None = None
    notes: str | None = None

    def __post_init__(self) -> None:
        if not self.company.name.strip():
            raise ValueError("Company name cannot be empty.")

        if not self.position.strip():
            raise ValueError("Position cannot be empty.")

        if not isinstance(self.application_type, ApplicationType):
            raise ValueError("Invalid application type.")

        if not isinstance(self.status, ApplicationStatus):
            raise ValueError("Invalid application status.")

        if self.deadline is not None and self.deadline < self.date_applied:
            raise ValueError("Deadline cannot be before the application date.")