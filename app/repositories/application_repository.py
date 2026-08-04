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

    def get_by_id(self, application_id: int) -> ApplicationDB | None:
        return self.session.get(ApplicationDB, application_id)

    def get_all(self) -> list[ApplicationDB]:
        return list(self.session.query(ApplicationDB).all())

    def get_by_company_id(self, company_id: int) -> list[ApplicationDB]:
        return list(
            self.session.query(ApplicationDB)
            .filter(ApplicationDB.company_id == company_id)
            .all()
        )

    def search(self, query: str) -> list[ApplicationDB]:
        search_term = f"%{query}%"

        return (
            self.session.query(ApplicationDB)
            .join(ApplicationDB.company)
            .filter(
                ApplicationDB.position.ilike(search_term)
                | CompanyDB.name.ilike(search_term)
            )
            .order_by(ApplicationDB.position)
            .all()
        )

    def update(self, application: ApplicationDB) -> ApplicationDB:
        self.session.commit()
        self.session.refresh(application)

        return application

    def delete(self, application: ApplicationDB) -> None:
        self.session.delete(application)
        self.session.commit()