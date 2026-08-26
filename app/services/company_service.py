from sqlalchemy.orm import Session

from app.database.models.company import CompanyDB
from app.repositories.company_repository import CompanyRepository


class CompanyService:
    def __init__(self, session: Session) -> None:
        self.repository = CompanyRepository(session)

    def create_company(
        self,
        name: str,
        website: str | None = None,
        industry: str | None = None,
        location: str | None = None,
        notes: str | None = None,
    ) -> CompanyDB:
        name = name.strip()

        if not name:
            raise ValueError("Company name cannot be empty.")

        company = CompanyDB(
            name=name,
            website=website.strip() if website else None,
            industry=industry.strip() if industry else None,
            location=location.strip() if location else None,
            notes=notes.strip() if notes else None,
        )

        return self.repository.create(company)

    def get_company(self, company_id: int) -> CompanyDB | None:
        return self.repository.get_by_id(company_id)

    def get_companies(self) -> list[CompanyDB]:
        return self.repository.get_all()

    def search_companies(self, query: str) -> list[CompanyDB]:
        query = query.strip()

        if not query:
            return []

        return self.repository.search(query)    

    def update_company(
        self,
        company_id: int,
        name: str | None = None,
        website: str | None = None,
        industry: str | None = None,
        location: str | None = None,
        notes: str | None = None,
    ) -> CompanyDB | None:
        company = self.repository.get_by_id(company_id)

        if company is None:
            return None

        if name is not None:
            if not name.strip():
                raise ValueError("Company name cannot be empty.")
            company.name = name.strip()

        if website is not None:
            company.website = website.strip() or None

        if industry is not None:
            company.industry = industry.strip() or None

        if location is not None:
            company.location = location.strip() or None

        if notes is not None:
            company.notes = notes.strip() or None

        return self.repository.update(company)

    def delete_company(self, company_id: int) -> bool:
        company = self.repository.get_by_id(company_id)

        if company is None:
            return False

        if company.applications:
            raise ValueError(
                f"Cannot delete company with {len(company.applications)} "
                "application(s)."
            )

        self.repository.delete(company)

        return True