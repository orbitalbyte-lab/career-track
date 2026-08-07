from datetime import date

from sqlalchemy.orm import Session

from app.database.models.application import ApplicationDB
from app.database.models.company import CompanyDB


class ApplicationRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, application: ApplicationDB) -> ApplicationDB:
        self.session.add(application)
        self.session.commit()
        self.session.refresh(application)

        return application

    def get_all(self) -> list[ApplicationDB]:
        return list(
            self.session.query(ApplicationDB).all()
        )

    def get_all_sorted_by_date(self) -> list[ApplicationDB]:
        return list(
            self.session.query(ApplicationDB)
            .order_by(
                ApplicationDB.date_applied.desc()
            )
            .all()
        )

    def get_by_company_id(self, company_id: int) -> list[ApplicationDB]:
        return list(
            self.session.query(ApplicationDB)
            .filter(ApplicationDB.company_id == company_id)
            .all()
        )

    def get_by_status(self, status: str) -> list[ApplicationDB]:
        return list(
            self.session.query(ApplicationDB)
            .filter(ApplicationDB.status == status)
            .order_by(ApplicationDB.position)
            .all()
        )

    def get_by_application_type(
        self,
        application_type: str,
    ) -> list[ApplicationDB]:
        return list(
            self.session.query(ApplicationDB)
            .filter(
                ApplicationDB.application_type == application_type
            )
            .order_by(ApplicationDB.position)
            .all()
        )

    def get_by_date(
        self,
        application_date: date,
    ) -> list[ApplicationDB]:
        return list(
            self.session.query(ApplicationDB)
            .filter(
                ApplicationDB.date_applied == application_date
            )
            .order_by(ApplicationDB.position)
            .all()
        )

    def get_by_deadline(
        self,
        deadline: date,
    ) -> list[ApplicationDB]:
        return list(
            self.session.query(ApplicationDB)
            .filter(
                ApplicationDB.deadline == deadline
            )
            .order_by(ApplicationDB.position)
            .all()
        )

    def search(self, query: str) -> list[ApplicationDB]:
        search_pattern = f"%{query}%"

        return (
            self.session.query(ApplicationDB)
            .join(ApplicationDB.company)
            .filter(
                (ApplicationDB.position.ilike(search_pattern))
                | (
                    ApplicationDB.company.has(
                        CompanyDB.name.ilike(search_pattern)
                    )
                )
                | (ApplicationDB.status.ilike(search_pattern))
                | (
                    ApplicationDB.application_type.ilike(
                        search_pattern
                    )
                )
            )
            .order_by(ApplicationDB.position)
            .all()
        )

    def count_all(self) -> int:
        return self.session.query(ApplicationDB).count()

    def count_by_status(self, status: str) -> int:
        return (
            self.session.query(ApplicationDB)
            .filter(
                ApplicationDB.status == status
            )
            .count()
        )

    def count_by_application_type(
        self,
        application_type: str,
    ) -> int:
        return (
            self.session.query(ApplicationDB)
            .filter(
                ApplicationDB.application_type == application_type
            )
            .count()
        )

    def get_by_id(self, application_id: int) -> ApplicationDB | None:
        return self.session.get(ApplicationDB, application_id)

    def update(self, application: ApplicationDB) -> ApplicationDB:
        self.session.commit()
        self.session.refresh(application)

        return application

    def delete(self, application: ApplicationDB) -> None:
        self.session.delete(application)
        self.session.commit()