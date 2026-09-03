from sqlalchemy.orm import Session

from app.database.models.company import CompanyDB


class CompanyRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, company: CompanyDB) -> CompanyDB:
        self.session.add(company)
        self.session.commit()
        self.session.refresh(company)

        return company

    def get_by_id(self, company_id: int) -> CompanyDB | None:
        return self.session.get(CompanyDB, company_id)

    def get_all(self) -> list[CompanyDB]:
        return self.session.query(CompanyDB).all()

    def search(self, query: str) -> list[CompanyDB]:
        return (
            self.session.query(CompanyDB)
            .filter(CompanyDB.name.ilike(f"%{query}%"))
            .order_by(CompanyDB.name)
            .all()
        )

    def update(self, company: CompanyDB) -> CompanyDB:
        self.session.commit()
        self.session.refresh(company)

        return company

    def delete(self, company: CompanyDB) -> None:
        self.session.delete(company)
        self.session.commit()
