from datetime import date

import pytest

from app.database.connection import Base, SessionLocal, engine
from app.database.init_db import initialize_database
from app.services.application_service import ApplicationService
from app.services.company_service import CompanyService


def setup_database():
    Base.metadata.drop_all(bind=engine)
    initialize_database()


def test_company_service_creates_company():
    setup_database()

    with SessionLocal() as session:
        service = CompanyService(session)

        company = service.create_company(
            name="Microsoft",
            industry="Technology",
            location="Redmond, WA",
        )

        assert company.id is not None
        assert company.name == "Microsoft"
        assert company.industry == "Technology"


def test_company_service_gets_company():
    setup_database()

    with SessionLocal() as session:
        service = CompanyService(session)

        created = service.create_company(name="Google")

        found = service.get_company(created.id)

        assert found is not None
        assert found.name == "Google"


def test_application_service_creates_application():
    setup_database()

    with SessionLocal() as session:
        company_service = CompanyService(session)
        application_service = ApplicationService(session)

        company = company_service.create_company(
            name="Microsoft",
            industry="Technology",
        )

        application = application_service.create_application(
            company_id=company.id,
            position="Software Engineering Intern",
            application_type="Internship",
            date_applied=date(2026, 7, 30),
            status="Applied",
        )

        assert application.id is not None
        assert application.company_id == company.id
        assert application.position == "Software Engineering Intern"


def test_application_service_rejects_unknown_company():
    setup_database()

    with SessionLocal() as session:
        service = ApplicationService(session)

        with pytest.raises(ValueError, match="Company not found"):
            service.create_application(
                company_id=9999,
                position="Software Engineering Intern",
                application_type="Internship",
                date_applied=date(2026, 7, 30),
                status="Applied",
            )


def test_application_service_gets_company_applications():
    setup_database()

    with SessionLocal() as session:
        company_service = CompanyService(session)
        application_service = ApplicationService(session)

        company = company_service.create_company(
            name="Google",
            industry="Technology",
        )

        application_service.create_application(
            company_id=company.id,
            position="Backend Engineering Intern",
            application_type="Internship",
            date_applied=date(2026, 7, 30),
            status="Applied",
        )

        applications = application_service.get_company_applications(
            company.id
        )

        assert len(applications) == 1
        assert applications[0].position == "Backend Engineering Intern"