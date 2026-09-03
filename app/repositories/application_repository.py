from datetime import date

from sqlalchemy.orm import Session

from app.database.models.application import ApplicationDB
from app.database.models.company import CompanyDB


class ApplicationRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create(
        self,
        application: ApplicationDB,
    ) -> ApplicationDB:
        self.session.add(application)
        self.session.commit()
        self.session.refresh(application)

        return application

    def get_all(self) -> list[ApplicationDB]:
        return self.session.query(ApplicationDB).all()

    def get_all_sorted_by_date(
        self,
    ) -> list[ApplicationDB]:
        return (
            self.session.query(ApplicationDB)
            .order_by(ApplicationDB.date_applied.desc())
            .all()
        )

    def get_by_company_id(
        self,
        company_id: int,
    ) -> list[ApplicationDB]:
        return (
            self.session.query(ApplicationDB)
            .filter(ApplicationDB.company_id == company_id)
            .all()
        )

    def get_by_status(
        self,
        status: str,
    ) -> list[ApplicationDB]:
        return (
            self.session.query(ApplicationDB)
            .filter(ApplicationDB.status == status)
            .order_by(ApplicationDB.position)
            .all()
        )

    def get_by_application_type(
        self,
        application_type: str,
    ) -> list[ApplicationDB]:
        return (
            self.session.query(ApplicationDB)
            .filter(ApplicationDB.application_type == application_type)
            .order_by(ApplicationDB.position)
            .all()
        )

    def get_by_date(
        self,
        application_date: date,
    ) -> list[ApplicationDB]:
        return (
            self.session.query(ApplicationDB)
            .filter(ApplicationDB.date_applied == application_date)
            .order_by(ApplicationDB.position)
            .all()
        )

    def get_by_deadline(
        self,
        deadline: date,
    ) -> list[ApplicationDB]:
        return (
            self.session.query(ApplicationDB)
            .filter(ApplicationDB.deadline == deadline)
            .order_by(ApplicationDB.position)
            .all()
        )

    def get_upcoming_deadlines(
        self,
        today: date,
        limit: int = 5,
    ) -> list[ApplicationDB]:
        return (
            self.session.query(ApplicationDB)
            .filter(
                ApplicationDB.deadline.isnot(None),
                ApplicationDB.deadline >= today,
            )
            .order_by(ApplicationDB.deadline.asc())
            .limit(limit)
            .all()
        )

    def filter_applications(
        self,
        status: str | None = None,
        application_type: str | None = None,
        company_id: int | None = None,
        date_applied: date | None = None,
    ) -> list[ApplicationDB]:
        query = self.session.query(ApplicationDB)

        if status is not None:
            query = query.filter(ApplicationDB.status == status)

        if application_type is not None:
            query = query.filter(ApplicationDB.application_type == application_type)

        if company_id is not None:
            query = query.filter(ApplicationDB.company_id == company_id)

        if date_applied is not None:
            query = query.filter(ApplicationDB.date_applied == date_applied)

        return query.order_by(ApplicationDB.date_applied.desc()).all()

    def search(
        self,
        query: str,
    ) -> list[ApplicationDB]:
        search_pattern = f"%{query}%"

        return (
            self.session.query(ApplicationDB)
            .join(ApplicationDB.company)
            .filter(
                ApplicationDB.position.ilike(search_pattern)
                | ApplicationDB.company.has(CompanyDB.name.ilike(search_pattern))
                | ApplicationDB.status.ilike(search_pattern)
                | ApplicationDB.application_type.ilike(search_pattern)
            )
            .order_by(ApplicationDB.position)
            .all()
        )

    def count_all(self) -> int:
        return self.session.query(ApplicationDB).count()

    def count_by_status(
        self,
        status: str,
    ) -> int:
        return (
            self.session.query(ApplicationDB)
            .filter(ApplicationDB.status == status)
            .count()
        )

    def count_by_application_type(
        self,
        application_type: str,
    ) -> int:
        return (
            self.session.query(ApplicationDB)
            .filter(ApplicationDB.application_type == application_type)
            .count()
        )

    def get_by_id(
        self,
        application_id: int,
    ) -> ApplicationDB | None:
        return self.session.get(
            ApplicationDB,
            application_id,
        )

    def get_total_count(self) -> int:
        return self.session.query(ApplicationDB).count()

    def get_application_type_counts(
        self,
    ) -> dict[str, int]:
        applications = self.get_all()
        statistics: dict[str, int] = {}

        for application in applications:
            application_type = application.application_type

            statistics[application_type] = statistics.get(application_type, 0) + 1

        return statistics

    def get_status_counts(
        self,
    ) -> dict[str, int]:
        applications = self.get_all()
        statistics: dict[str, int] = {}

        for application in applications:
            status = application.status

            statistics[status] = statistics.get(status, 0) + 1

        return statistics

    def get_company_statistics(
        self,
    ) -> dict[str, int]:
        applications = (
            self.session.query(ApplicationDB).join(ApplicationDB.company).all()
        )

        statistics: dict[str, int] = {}

        for application in applications:
            company_name = application.company.name

            statistics[company_name] = statistics.get(company_name, 0) + 1

        return statistics

    def get_monthly_application_counts(
        self,
    ) -> dict[str, int]:
        applications = self.get_all()
        statistics: dict[str, int] = {}

        for application in applications:
            month = application.date_applied.strftime("%Y-%m")

            statistics[month] = statistics.get(month, 0) + 1

        return statistics

    def get_location_statistics(
        self,
    ) -> dict[str, int]:
        applications = self.get_all()
        statistics: dict[str, int] = {}

        for application in applications:
            location = application.location or "Not specified"

            statistics[location] = statistics.get(location, 0) + 1

        return statistics

    def get_all_sorted(
        self,
        field: str,
    ) -> list[ApplicationDB]:
        query = self.session.query(ApplicationDB)

        if field == "date":
            return query.order_by(ApplicationDB.date_applied.desc()).all()

        if field == "position":
            return query.order_by(ApplicationDB.position).all()

        return query.all()

    def update(
        self,
        application: ApplicationDB,
    ) -> ApplicationDB:
        self.session.commit()
        self.session.refresh(application)

        return application

    def delete(
        self,
        application: ApplicationDB,
    ) -> None:
        self.session.delete(application)
        self.session.commit()
