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
    def get_by_id_for_user(
        self,
        company_id: int,
        user_id: int,
    ) -> CompanyDB | None:
        return (
            self.session.query(CompanyDB)
            .filter(
                CompanyDB.id == company_id,
                CompanyDB.user_id == user_id,
            )
            .first()
        )

    def get_all(
        self,
        offset: int = 0,
        limit: int | None = None,
    ) -> list[CompanyDB]:
        query = self.session.query(CompanyDB).order_by(CompanyDB.id)

        if offset > 0:
            query = query.offset(offset)

        if limit is not None:
            query = query.limit(limit)

        return query.all()

    def get_all_for_user(
        self,
        user_id: int,
        offset: int = 0,
        limit: int | None = None,
    ) -> list[CompanyDB]:
        query = (
            self.session.query(CompanyDB)
            .filter(CompanyDB.user_id == user_id)
            .order_by(CompanyDB.id)
        )

        if offset > 0:
            query = query.offset(offset)

        if limit is not None:
            query = query.limit(limit)

        return query.all()
    def search(self, query: str) -> list[CompanyDB]:
        return (
            self.session.query(CompanyDB)
            .filter(CompanyDB.name.ilike(f"%{query}%"))
            .order_by(CompanyDB.name)
            .all()
        )

    def search_for_user(
        self,
        query: str,
        user_id: int,
    ) -> list[CompanyDB]:
        return (
            self.session.query(CompanyDB)
            .filter(
                CompanyDB.user_id == user_id,
                CompanyDB.name.ilike(f"%{query}%"),
            )
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
