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

    def search_applications(
        self,
        query: str,
    ) -> list[ApplicationDB]:
        if not query.strip():
            return []

        return self.application_repository.search(query.strip())

    def update_application(
        self,
        application_id: int,
        position: str | None = None,
        application_type: str | None = None,
        date_applied: date | None = None,
        status: str | None = None,
        location: str | None = None,
        deadline: date | None = None,
        job_url: str | None = None,
        notes: str | None = None,
    ) -> ApplicationDB | None:
        application = self.application_repository.get_by_id(
            application_id
        )

        if application is None:
            return None

        if position is not None:
            if not position.strip():
                raise ValueError("Position cannot be empty.")
            application.position = position.strip()

        if application_type is not None:
            application.application_type = application_type.strip()

        if date_applied is not None:
            application.date_applied = date_applied

        if status is not None:
            application.status = status.strip()

        if location is not None:
            application.location = location.strip() or None

        if deadline is not None:
            if deadline < application.date_applied:
                raise ValueError(
                    "Deadline cannot be before the application date"
                )
            application.deadline = deadline

        if job_url is not None:
            application.job_url = job_url.strip() or None

        if notes is not None:
            application.notes = notes.strip() or None

        return self.application_repository.update(application)

    def get_company_applications(
        self,
        company_id: int,
    ) -> list[ApplicationDB]:
        return self.application_repository.get_by_company_id(
            company_id
        )

    def get_applications_by_status(
        self,
        status: str,
    ) -> list[ApplicationDB]:
        if not status.strip():
            return []

        return self.application_repository.get_by_status(
            status.strip()
        )

    def get_applications_by_date(
        self,
        application_date: date,
    ) -> list[ApplicationDB]:
        return self.application_repository.get_by_date(
            application_date
        )

    def get_applications_by_deadline(
        self,
        deadline: date,
    ) -> list[ApplicationDB]:
        return self.application_repository.get_by_deadline(
            deadline
        )

    def get_applications_by_application_type(
        self,
        application_type: str,
    ) -> list[ApplicationDB]:
        if not application_type.strip():
            return []

        return self.application_repository.get_by_application_type(
            application_type.strip()
        )

    def filter_applications(
        self,
        status: str | None = None,
        application_type: str | None = None,
        company_id: int | None = None,
        date_applied: date | None = None,
    ) -> list[ApplicationDB]:
       if status is not None:
           status = status.strip()

           if not status:
               status = None

       if application_type is not None:
           application_type = application_type.strip()

           if not application_type:
               application_type = None

       return self.application_repository.filter_applications(
           status=status,
           application_type=application_type,
           company_id=company_id,
           date_applied=date_applied,
       )

    def get_total_applications(self) -> int:
        return self.application_repository.get_total_count()

    def get_applications_count_by_status(
        self,
        status: str,
    ) -> int:
        if not status.strip():
            return 0

        return self.application_repository.count_by_status(
            status.strip()
        )

    def get_applications_count_by_type(
        self,
        application_type: str,
    ) -> int:
        if not application_type.strip():
            return 0

        return self.application_repository.count_by_application_type(
            application_type.strip()
        )

    def get_application_type_statistics(
        self,
    ) -> dict[str, int]:
        return self.application_repository.get_application_type_counts()

    def get_status_statistics(
        self,
    ) -> dict[str, int]:
        return self.application_repository.get_status_counts()
    def get_company_statistics(
        self,
    ) -> dict[str, int]:
        return self.application_repository.get_company_statistics()

    def get_location_statistics(
        self,
    ) -> dict[str, int]:
        return self.application_repository.get_location_statistics()
    def get_dashboard_statistics(self) -> dict:
        total = self.application_repository.get_total_count()

        by_status = self.application_repository.get_status_counts()

        successful_applications = by_status.get("Offer", 0)

        success_rate = (
            (successful_applications / total) * 100
            if total > 0
            else 0.0
        )

        return {
            "total": total,
            "total_companies": len(
                self.company_repository.get_all()
            ),
            "by_status": by_status,
            "by_application_type": (
                self.application_repository
                .get_application_type_counts()
            ),
            "by_company": (
                self.application_repository
                .get_company_statistics()
            ),
            "success_rate": success_rate,
        }

    def get_recent_applications(
        self,
    ) -> list[ApplicationDB]:
        return self.application_repository.get_all_sorted_by_date()[:5]
    def get_monthly_application_counts(
        self,
    ) -> dict[str, int]:
        return self.application_repository.get_monthly_application_counts()
    def get_upcoming_deadlines(
        self,
        today: date,
        limit: int = 5,
    ) -> list[ApplicationDB]:
        if limit <= 0:
            return []

        return self.application_repository.get_upcoming_deadlines(
            today=today,
            limit=limit,
        )
    def delete_application(
        self,
        application_id: int,
    ) -> bool:
        application = self.application_repository.get_by_id(
            application_id
        )

        if application is None:
            return False

        self.application_repository.delete(application)

        return True
