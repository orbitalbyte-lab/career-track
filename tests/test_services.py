from datetime import date

import pytest

from app.database.connection import Base, SessionLocal, engine
from app.database.init_db import initialize_database
from app.database.models.company import CompanyDB
from app.repositories.company_repository import CompanyRepository
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


def test_company_service_updates_company():
    setup_database()

    with SessionLocal() as session:
        service = CompanyService(session)

        company = service.create_company(
            name="Google",
            industry="Technology",
            location="Mountain View",
        )

        updated = service.update_company(
            company_id=company.id,
            name="Google LLC",
            industry="Internet Technology",
            location="California",
            website="https://google.com",
            notes="Target company",
        )

        assert updated is not None
        assert updated.name == "Google LLC"
        assert updated.industry == "Internet Technology"
        assert updated.location == "California"
        assert updated.website == "https://google.com"
        assert updated.notes == "Target company"


def test_company_service_update_keeps_existing_values():
    setup_database()

    with SessionLocal() as session:
        service = CompanyService(session)

        company = service.create_company(
            name="Microsoft",
            industry="Technology",
            location="Redmond",
        )

        updated = service.update_company(
            company_id=company.id,
            name="Microsoft Corporation",
        )

        assert updated is not None
        assert updated.name == "Microsoft Corporation"
        assert updated.industry == "Technology"
        assert updated.location == "Redmond"


def test_company_service_update_unknown_company():
    setup_database()

    with SessionLocal() as session:
        service = CompanyService(session)

        updated = service.update_company(
            company_id=9999,
            name="Unknown Company",
        )

        assert updated is None


def test_company_service_rejects_empty_updated_name():
    setup_database()

    with SessionLocal() as session:
        service = CompanyService(session)

        company = service.create_company(
            name="Google",
        )

        with pytest.raises(
            ValueError,
            match="Company name cannot be empty",
        ):
            service.update_company(
                company_id=company.id,
                name="   ",
            )


def test_company_service_deletes_company_without_applications():
    setup_database()

    with SessionLocal() as session:
        service = CompanyService(session)

        company = service.create_company(
            name="Microsoft",
        )

        result = service.delete_company(company.id)

        assert result is True
        assert service.get_company(company.id) is None


def test_company_service_rejects_deleting_company_with_applications():
    setup_database()

    with SessionLocal() as session:
        company_service = CompanyService(session)
        application_service = ApplicationService(session)

        company = company_service.create_company(
            name="Google",
        )

        application_service.create_application(
            company_id=company.id,
            position="Software Engineering Intern",
            application_type="Internship",
            date_applied=date(2026, 7, 30),
            status="Applied",
        )

        with pytest.raises(
            ValueError,
            match="Cannot delete company with 1 application",
        ):
            company_service.delete_company(company.id)

        assert company_service.get_company(company.id) is not None


def test_company_service_searches_companies():
    setup_database()

    with SessionLocal() as session:
        service = CompanyService(session)

        service.create_company(name="Microsoft")
        service.create_company(name="Google")
        service.create_company(name="Microsoft Azure")

        results = service.search_companies("microsoft")

        assert len(results) == 2
        assert results[0].name == "Microsoft"
        assert results[1].name == "Microsoft Azure"


def test_company_service_search_returns_empty_for_blank_query():
    setup_database()

    with SessionLocal() as session:
        service = CompanyService(session)

        service.create_company(name="Microsoft")

        results = service.search_companies("   ")

        assert results == []


def test_application_service_gets_application():
    setup_database()

    with SessionLocal() as session:
        company_service = CompanyService(session)
        application_service = ApplicationService(session)

        company = company_service.create_company(
            name="Google",
            industry="Technology",
        )

        created = application_service.create_application(
            company_id=company.id,
            position="Software Engineering Intern",
            application_type="Internship",
            date_applied=date(2026, 7, 30),
            status="Applied",
            location="Remote",
            deadline=date(2026, 8, 15),
            job_url="https://careers.google.com",
            notes="Excellent internship opportunity.",
        )

        found = application_service.get_application(created.id)

        assert found is not None
        assert found.id == created.id
        assert found.position == "Software Engineering Intern"
        assert found.status == "Applied"
        assert found.location == "Remote"
        assert found.deadline == date(2026, 8, 15)
        assert found.job_url == "https://careers.google.com"
        assert found.notes == "Excellent internship opportunity."


def test_application_service_updates_application():
    setup_database()

    with SessionLocal() as session:
        company_service = CompanyService(session)
        application_service = ApplicationService(session)

        company = company_service.create_company(
            name="Google",
        )

        application = application_service.create_application(
            company_id=company.id,
            position="Software Engineering Intern",
            application_type="Internship",
            date_applied=date(2026, 7, 30),
            status="Applied",
            location="Remote",
            deadline=date(2026, 8, 15),
            job_url="https://careers.google.com",
            notes="Original notes",
        )

        updated = application_service.update_application(
            application_id=application.id,
            position="Backend Engineering Intern",
            status="Interview",
            location="Mountain View",
            deadline=date(2026, 8, 20),
            job_url="https://careers.google.com/backend",
            notes="Passed initial screening.",
        )

        assert updated is not None
        assert updated.position == "Backend Engineering Intern"
        assert updated.status == "Interview"
        assert updated.location == "Mountain View"
        assert updated.deadline == date(2026, 8, 20)
        assert updated.job_url == "https://careers.google.com/backend"
        assert updated.notes == "Passed initial screening."


def test_application_service_update_keeps_existing_values():
    setup_database()

    with SessionLocal() as session:
        company_service = CompanyService(session)
        application_service = ApplicationService(session)

        company = company_service.create_company(
            name="Microsoft",
        )

        application = application_service.create_application(
            company_id=company.id,
            position="Software Engineering Intern",
            application_type="Internship",
            date_applied=date(2026, 7, 30),
            status="Applied",
            location="Redmond",
            notes="Original notes",
        )

        updated = application_service.update_application(
            application_id=application.id,
            position="Software Engineer Intern",
        )

        assert updated is not None
        assert updated.position == "Software Engineer Intern"
        assert updated.status == "Applied"
        assert updated.location == "Redmond"
        assert updated.notes == "Original notes"


def test_application_service_deletes_application():
    setup_database()

    with SessionLocal() as session:
        company_service = CompanyService(session)
        application_service = ApplicationService(session)

        company = company_service.create_company(
            name="Google",
        )

        application = application_service.create_application(
            company_id=company.id,
            position="Software Engineering Intern",
            application_type="Internship",
            date_applied=date(2026, 8, 4),
            status="Applied",
        )

        result = application_service.delete_application(application.id)

        assert result is True
        assert application_service.get_application(application.id) is None


def test_application_service_delete_unknown_application():
    setup_database()

    with SessionLocal() as session:
        application_service = ApplicationService(session)

        result = application_service.delete_application(9999)

        assert result is False


def test_application_service_searches_applications():
    setup_database()

    with SessionLocal() as session:
        company_service = CompanyService(session)
        application_service = ApplicationService(session)

        company = company_service.create_company(
            name="Google",
        )

        application_service.create_application(
            company_id=company.id,
            position="Software Engineering Intern",
            application_type="Internship",
            date_applied=date(2026, 8, 4),
            status="Applied",
        )

        application_service.create_application(
            company_id=company.id,
            position="Backend Engineering Intern",
            application_type="Internship",
            date_applied=date(2026, 8, 4),
            status="Applied",
        )

        application_service.create_application(
            company_id=company.id,
            position="Data Analyst Intern",
            application_type="Internship",
            date_applied=date(2026, 8, 4),
            status="Applied",
        )

        results = application_service.search_applications("engineering")

        assert len(results) == 2
        assert results[0].position == "Backend Engineering Intern"
        assert results[1].position == "Software Engineering Intern"


def test_application_service_search_returns_empty_for_blank_query():
    setup_database()

    with SessionLocal() as session:
        application_service = ApplicationService(session)

        results = application_service.search_applications("   ")

        assert results == []


def test_application_service_searches_by_company_name():
    setup_database()

    with SessionLocal() as session:
        company_repository = CompanyRepository(session)
        application_service = ApplicationService(session)

        company = company_repository.create(
            CompanyDB(name="Microsoft")
        )

        application_service.create_application(
            company_id=company.id,
            position="Software Engineer",
            application_type="Full-time",
            date_applied=date(2026, 8, 4),
            status="Applied",
        )

        results = application_service.search_applications("microsoft")

        assert len(results) == 1
        assert results[0].company.name == "Microsoft"


def test_application_service_searches_by_status():
    setup_database()

    with SessionLocal() as session:
        company_repository = CompanyRepository(session)
        application_service = ApplicationService(session)

        company = company_repository.create(
            CompanyDB(name="Google")
        )

        application_service.create_application(
            company_id=company.id,
            position="Software Engineer",
            application_type="Full-time",
            date_applied=date(2026, 8, 4),
            status="Interview",
        )

        results = application_service.search_applications("interview")

        assert len(results) == 1
        assert results[0].status == "Interview"


def test_application_service_searches_by_application_type():
    setup_database()

    with SessionLocal() as session:
        company_repository = CompanyRepository(session)
        application_service = ApplicationService(session)

        company = company_repository.create(
            CompanyDB(name="Amazon")
        )

        application_service.create_application(
            company_id=company.id,
            position="Software Engineer Intern",
            application_type="Internship",
            date_applied=date(2026, 8, 4),
            status="Applied",
        )

        results = application_service.search_applications("internship")

        assert len(results) == 1
        assert results[0].application_type == "Internship"

def test_application_service_filters_by_status():
    setup_database()

    with SessionLocal() as session:
        company_service = CompanyService(session)
        application_service = ApplicationService(session)

        company = company_service.create_company(
            name="Google",
        )

        application_service.create_application(
            company_id=company.id,
            position="Software Engineer",
            application_type="Full-time",
            date_applied=date(2026, 8, 4),
            status="Applied",
        )

        application_service.create_application(
            company_id=company.id,
            position="Backend Engineer",
            application_type="Full-time",
            date_applied=date(2026, 8, 4),
            status="Interview",
        )

        application_service.create_application(
            company_id=company.id,
            position="Data Analyst",
            application_type="Internship",
            date_applied=date(2026, 8, 4),
            status="Rejected",
        )

        results = application_service.get_applications_by_status(
            "Interview"
        )

        assert len(results) == 1
        assert results[0].position == "Backend Engineer"
        assert results[0].status == "Interview"

def test_application_service_status_filter_returns_empty_for_blank_status():
    setup_database()

    with SessionLocal() as session:
        application_service = ApplicationService(session)

        results = application_service.get_applications_by_status("   ")

        assert results == []

def test_application_service_filters_by_application_type():
    setup_database()

    with SessionLocal() as session:
        company_service = CompanyService(session)
        application_service = ApplicationService(session)

        company = company_service.create_company(
            name="Microsoft",
        )

        application_service.create_application(
            company_id=company.id,
            position="Software Engineer",
            application_type="Full-time",
            date_applied=date(2026, 8, 4),
            status="Applied",
        )

        application_service.create_application(
            company_id=company.id,
            position="Software Engineering Intern",
            application_type="Internship",
            date_applied=date(2026, 8, 4),
            status="Applied",
        )

        application_service.create_application(
            company_id=company.id,
            position="Backend Intern",
            application_type="Internship",
            date_applied=date(2026, 8, 4),
            status="Interview",
        )

        results = application_service.get_applications_by_application_type(
            "Internship"
        )

        assert len(results) == 2
        assert results[0].application_type == "Internship"
        assert results[1].application_type == "Internship"

def test_application_service_filters_by_date():
    setup_database()

    with SessionLocal() as session:
        company_service = CompanyService(session)
        application_service = ApplicationService(session)

        company = company_service.create_company(
            name="Google",
        )

        application_service.create_application(
            company_id=company.id,
            position="Backend Engineer",
            application_type="Full-time",
            date_applied=date(2026, 8, 4),
            status="Applied",
        )

        application_service.create_application(
            company_id=company.id,
            position="Software Engineer",
            application_type="Full-time",
            date_applied=date(2026, 8, 5),
            status="Interview",
        )

        results = application_service.get_applications_by_date(
            date(2026, 8, 4)
        )

        assert len(results) == 1
        assert results[0].position == "Backend Engineer"
        assert results[0].date_applied == date(2026, 8, 4)
