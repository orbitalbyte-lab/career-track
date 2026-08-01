from datetime import date

from sqlalchemy.orm import Session

from app.database.models.application import ApplicationDB
from app.repositories.application_repository import ApplicationRepository
from app.repositories.company_repository import CompanyRepository


class ApplicationService:
    def __init__(self, session: Session) -> None:
        self.application_repository = ApplicationRepository(session)
        self.company_repository = CompanyRepository(session)

    def create_application(
        self,
        company_id: int,
        position: str,
        application_type: str,
        date_applied: date,
        status: str,
        location: str | None = None,
        deadline: date | None = None,
        job_url: str | None = None,
        notes: str | None = None,
    ) -> ApplicationDB:
        company = self.company_repository.get_by_id(company_id)

        if company is None:
            raise ValueError("Company not found")

        application = ApplicationDB(
            company_id=company_id,
            position=position,
            application_type=application_type,
            date_applied=date_applied,
            status=status,
            location=location,
            deadline=deadline,
            job_url=job_url,
            notes=notes,
        )

        return self.application_repository.create(application)

    def get_application(
        self,
        application_id: int,
    ) -> ApplicationDB | None:
        return self.application_repository.get_by_id(application_id)

    def get_applications(self) -> list[ApplicationDB]:
        return self.application_repository.get_all()

    def get_company_applications(
        self,
        company_id: int,
    ) -> list[ApplicationDB]:
        return self.application_repository.get_by_company_id(company_id)

    def delete_application(self, application_id: int) -> bool:
        application = self.application_repository.get_by_id(application_id)

        if application is None:
            return False

        self.application_repository.delete(application)

        return True