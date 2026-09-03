from datetime import UTC, date, datetime

import pytest

from app.database.connection import Base, SessionLocal, engine
from app.database.init_db import initialize_database
from app.database.models.company import CompanyDB
from app.models.follow_up import FollowUp
from app.models.interview import (
    Interview,
    InterviewOutcome,
    InterviewStatus,
    InterviewType,
)
from app.repositories.company_repository import CompanyRepository
from app.services.application_service import ApplicationService
from app.services.company_service import CompanyService
from app.services.follow_up_service import FollowUpService
from app.services.import_service import ImportService
from app.services.interview_service import InterviewService


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

        applications = application_service.get_company_applications(company.id)

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


def test_application_service_update_unknown_application():
    setup_database()

    with SessionLocal() as session:
        application_service = ApplicationService(session)

        result = application_service.update_application(
            application_id=9999,
            position="Software Engineer",
        )

        assert result is None


def test_application_service_rejects_empty_updated_position():
    setup_database()

    with SessionLocal() as session:
        company_service = CompanyService(session)
        application_service = ApplicationService(session)

        company = company_service.create_company(
            name="Google",
        )

        application = application_service.create_application(
            company_id=company.id,
            position="Software Engineer",
            application_type="Full-time",
            date_applied=date(2026, 8, 4),
            status="Applied",
        )

        with pytest.raises(
            ValueError,
            match="Position cannot be empty",
        ):
            application_service.update_application(
                application_id=application.id,
                position="   ",
            )


def test_application_service_updates_all_optional_fields():
    setup_database()

    with SessionLocal() as session:
        company_service = CompanyService(session)
        application_service = ApplicationService(session)

        company = company_service.create_company(
            name="Microsoft",
        )

        application = application_service.create_application(
            company_id=company.id,
            position="Software Engineer",
            application_type="Internship",
            date_applied=date(2026, 8, 1),
            status="Applied",
            location="Remote",
            notes="Original",
        )

        updated = application_service.update_application(
            application_id=application.id,
            application_type=" Full-time ",
            date_applied=date(2026, 8, 5),
            status=" Interview ",
            location=" ",
            job_url=" ",
            notes=" ",
            deadline=date(2026, 8, 20),
        )

        assert updated is not None
        assert updated.application_type == "Full-time"
        assert updated.date_applied == date(2026, 8, 5)
        assert updated.status == "Interview"
        assert updated.location is None
        assert updated.job_url is None
        assert updated.notes is None
        assert updated.deadline == date(2026, 8, 20)


def test_application_service_rejects_deadline_before_application_date():
    setup_database()

    with SessionLocal() as session:
        company_service = CompanyService(session)
        application_service = ApplicationService(session)

        company = company_service.create_company(
            name="Google",
        )

        application = application_service.create_application(
            company_id=company.id,
            position="Software Engineer",
            application_type="Full-time",
            date_applied=date(2026, 8, 10),
            status="Applied",
        )

        with pytest.raises(
            ValueError,
            match="Deadline cannot be before the application date",
        ):
            application_service.update_application(
                application_id=application.id,
                deadline=date(2026, 8, 9),
            )


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

        company = company_repository.create(CompanyDB(name="Microsoft"))

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

        company = company_repository.create(CompanyDB(name="Google"))

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

        company = company_repository.create(CompanyDB(name="Amazon"))

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

        results = application_service.get_applications_by_status("Interview")

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

        results = application_service.get_applications_by_application_type("Internship")

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

        results = application_service.get_applications_by_date(date(2026, 8, 4))

        assert len(results) == 1
        assert results[0].position == "Backend Engineer"
        assert results[0].date_applied == date(2026, 8, 4)


def test_application_service_filters_by_deadline():
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
            deadline=date(2026, 8, 20),
            status="Applied",
        )

        application_service.create_application(
            company_id=company.id,
            position="Software Engineer",
            application_type="Full-time",
            date_applied=date(2026, 8, 5),
            deadline=date(2026, 8, 25),
            status="Interview",
        )

        results = application_service.get_applications_by_deadline(date(2026, 8, 20))

        assert len(results) == 1
        assert results[0].position == "Backend Engineer"
        assert results[0].deadline == date(2026, 8, 20)


def test_application_service_filters_blank_optional_values():
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
            application_type="Internship",
            date_applied=date(2026, 8, 4),
            status="Applied",
        )

        results = application_service.filter_applications(
            status="   ",
            application_type="   ",
        )

        assert len(results) == 1
        assert results[0].position == "Software Engineer"


def test_application_service_returns_zero_for_blank_status_count():
    setup_database()

    with SessionLocal() as session:
        application_service = ApplicationService(session)

        result = application_service.get_applications_count_by_status("   ")

        assert result == 0


def test_application_service_returns_zero_for_blank_type_count():
    setup_database()

    with SessionLocal() as session:
        application_service = ApplicationService(session)

        result = application_service.get_applications_count_by_type("   ")

        assert result == 0


def test_application_service_gets_total_applications_count():
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
            date_applied=date(2026, 8, 5),
            status="Interview",
        )

        result = application_service.get_total_applications()

        assert result == 2


def test_application_service_counts_applications_by_status():
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
            position="Backend Engineer",
            application_type="Full-time",
            date_applied=date(2026, 8, 5),
            status="Interview",
        )

        result = application_service.get_applications_count_by_status("Interview")

        assert result == 1


def test_application_service_counts_applications_by_type():
    setup_database()

    with SessionLocal() as session:
        company_service = CompanyService(session)
        application_service = ApplicationService(session)

        company = company_service.create_company(
            name="Amazon",
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
            position="Cloud Intern",
            application_type="Internship",
            date_applied=date(2026, 8, 5),
            status="Applied",
        )

        result = application_service.get_applications_count_by_type("Internship")

        assert result == 1


def test_application_service_gets_total_applications():
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
            application_type="Internship",
            date_applied=date(2026, 8, 5),
            status="Interview",
        )

        result = application_service.get_total_applications()

        assert result == 2


def test_application_service_gets_applications_by_status_count():
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
            position="Backend Engineer",
            application_type="Full-time",
            date_applied=date(2026, 8, 5),
            status="Interview",
        )

        application_service.create_application(
            company_id=company.id,
            position="Frontend Engineer",
            application_type="Full-time",
            date_applied=date(2026, 8, 6),
            status="Applied",
        )

        result = application_service.get_status_statistics()

        assert result["Applied"] == 2
        assert result["Interview"] == 1


def test_application_service_gets_applications_by_application_type_count():
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
            position="Backend Engineer",
            application_type="Internship",
            date_applied=date(2026, 8, 5),
            status="Interview",
        )

        application_service.create_application(
            company_id=company.id,
            position="Frontend Engineer",
            application_type="Full-time",
            date_applied=date(2026, 8, 6),
            status="Applied",
        )

        result = application_service.get_application_type_statistics()

        assert result == {
            "Full-time": 2,
            "Internship": 1,
        }


def test_application_service_gets_applications_by_company_count():
    setup_database()

    with SessionLocal() as session:
        company_service = CompanyService(session)
        application_service = ApplicationService(session)

        microsoft = company_service.create_company(
            name="Microsoft",
        )

        google = company_service.create_company(
            name="Google",
        )

        application_service.create_application(
            company_id=microsoft.id,
            position="Software Engineer",
            application_type="Full-time",
            date_applied=date(2026, 8, 4),
            status="Applied",
        )

        application_service.create_application(
            company_id=microsoft.id,
            position="Backend Engineer",
            application_type="Full-time",
            date_applied=date(2026, 8, 5),
            status="Interview",
        )

        application_service.create_application(
            company_id=google.id,
            position="Frontend Engineer",
            application_type="Internship",
            date_applied=date(2026, 8, 6),
            status="Applied",
        )

        result = application_service.get_company_statistics()

        assert result == {
            "Microsoft": 2,
            "Google": 1,
        }


def test_application_service_gets_location_statistics():
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
            date_applied=date(2026, 7, 10),
            status="Applied",
            location="Remote",
        )

        application_service.create_application(
            company_id=company.id,
            position="Backend Engineer",
            application_type="Full-time",
            date_applied=date(2026, 7, 20),
            status="Interview",
            location="Remote",
        )

        application_service.create_application(
            company_id=company.id,
            position="Frontend Engineer",
            application_type="Internship",
            date_applied=date(2026, 8, 5),
            status="Applied",
            location="Addis Ababa",
        )

        application_service.create_application(
            company_id=company.id,
            position="Data Analyst",
            application_type="Internship",
            date_applied=date(2026, 8, 8),
            status="Applied",
        )

        result = application_service.get_location_statistics()

        assert result == {
            "Remote": 2,
            "Addis Ababa": 1,
            "Not specified": 1,
        }


def test_application_service_gets_dashboard_statistics():
    setup_database()

    with SessionLocal() as session:
        company_service = CompanyService(session)
        application_service = ApplicationService(session)

        microsoft = company_service.create_company(
            name="Microsoft",
        )

        google = company_service.create_company(
            name="Google",
        )

        application_service.create_application(
            company_id=microsoft.id,
            position="Software Engineer",
            application_type="Full-time",
            date_applied=date(2026, 8, 4),
            status="Applied",
        )

        application_service.create_application(
            company_id=microsoft.id,
            position="Backend Engineer",
            application_type="Full-time",
            date_applied=date(2026, 8, 5),
            status="Interview",
        )

        application_service.create_application(
            company_id=google.id,
            position="Frontend Engineer",
            application_type="Internship",
            date_applied=date(2026, 8, 6),
            status="Applied",
        )

        result = application_service.get_dashboard_statistics()

        assert result == {
            "total": 3,
            "total_companies": 2,
            "by_status": {
                "Applied": 2,
                "Interview": 1,
            },
            "by_application_type": {
                "Full-time": 2,
                "Internship": 1,
            },
            "by_company": {
                "Microsoft": 2,
                "Google": 1,
            },
            "success_rate": 0.0,
        }


def test_application_service_calculates_success_rate():
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
            status="Offer",
        )

        application_service.create_application(
            company_id=company.id,
            position="Backend Engineer",
            application_type="Full-time",
            date_applied=date(2026, 8, 5),
            status="Applied",
        )

        application_service.create_application(
            company_id=company.id,
            position="Frontend Engineer",
            application_type="Internship",
            date_applied=date(2026, 8, 6),
            status="Rejected",
        )

        result = application_service.get_dashboard_statistics()

        assert result["success_rate"] == pytest.approx(33.33333333333333)


def test_application_service_filter_applications_by_status():
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
            position="Backend Engineer",
            application_type="Full-time",
            date_applied=date(2026, 8, 5),
            status="Interview",
        )

        result = application_service.filter_applications(
            status="Interview",
        )

        assert len(result) == 1
        assert result[0].position == "Backend Engineer"

def test_application_service_filters_by_company():
    setup_database()

    with SessionLocal() as session:
        company_service = CompanyService(session)
        application_service = ApplicationService(session)

        microsoft = company_service.create_company(
            name="Microsoft",
        )

        google = company_service.create_company(
            name="Google",
        )

        application_service.create_application(
            company_id=microsoft.id,
            position="Software Engineer",
            application_type="Full-time",
            date_applied=date(2026, 8, 4),
            status="Applied",
        )

        application_service.create_application(
            company_id=google.id,
            position="Frontend Engineer",
            application_type="Full-time",
            date_applied=date(2026, 8, 5),
            status="Applied",
        )

        result = application_service.filter_applications(
            company_id=microsoft.id,
        )

        assert len(result) == 1
        assert result[0].position == "Software Engineer"


def test_application_service_filters_by_multiple_fields():
    setup_database()

    with SessionLocal() as session:
        company_service = CompanyService(session)
        application_service = ApplicationService(session)

        microsoft = company_service.create_company(
            name="Microsoft",
        )

        application_service.create_application(
            company_id=microsoft.id,
            position="Software Engineer",
            application_type="Full-time",
            date_applied=date(2026, 8, 4),
            status="Applied",
        )

        application_service.create_application(
            company_id=microsoft.id,
            position="Backend Engineer",
            application_type="Full-time",
            date_applied=date(2026, 8, 5),
            status="Interview",
        )

        result = application_service.filter_applications(
            status="Interview",
            application_type="Full-time",
            company_id=microsoft.id,
        )

        assert len(result) == 1
        assert result[0].position == "Backend Engineer"


def test_application_service_gets_upcoming_deadlines():
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
            date_applied=date(2026, 8, 1),
            status="Applied",
            deadline=date(2026, 8, 15),
        )

        application_service.create_application(
            company_id=company.id,
            position="Backend Engineer",
            application_type="Full-time",
            date_applied=date(2026, 8, 2),
            status="Interview",
            deadline=date(2026, 8, 10),
        )

        application_service.create_application(
            company_id=company.id,
            position="Frontend Engineer",
            application_type="Internship",
            date_applied=date(2026, 8, 3),
            status="Applied",
            deadline=date(2026, 8, 5),
        )

        result = application_service.get_upcoming_deadlines(
            today=date(2026, 8, 8),
        )

        assert len(result) == 2
        assert result[0].position == "Backend Engineer"
        assert result[1].position == "Software Engineer"


def test_application_service_gets_monthly_application_counts():
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
            date_applied=date(2026, 7, 10),
            status="Applied",
        )

        application_service.create_application(
            company_id=company.id,
            position="Backend Engineer",
            application_type="Full-time",
            date_applied=date(2026, 7, 20),
            status="Interview",
        )

        application_service.create_application(
            company_id=company.id,
            position="Frontend Engineer",
            application_type="Internship",
            date_applied=date(2026, 8, 5),
            status="Applied",
        )

        result = application_service.get_monthly_application_counts()

        assert result == {
            "2026-07": 2,
            "2026-08": 1,
        }


def test_application_service_gets_applications_by_status_with_valid_status():
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

        results = application_service.get_applications_by_status(" Applied ")

        assert len(results) == 1
        assert results[0].status == "Applied"


def test_application_service_application_type_returns_empty_for_blank_type():
    setup_database()

    with SessionLocal() as session:
        application_service = ApplicationService(session)

        results = application_service.get_applications_by_application_type("   ")

        assert results == []


def test_application_service_gets_applications_by_application_type_with_valid_type():
    setup_database()

    with SessionLocal() as session:
        company_service = CompanyService(session)
        application_service = ApplicationService(session)

        company = company_service.create_company(
            name="Microsoft",
        )

        application_service.create_application(
            company_id=company.id,
            position="Software Engineering Intern",
            application_type="Internship",
            date_applied=date(2026, 8, 4),
            status="Applied",
        )

        results = application_service.get_applications_by_application_type(
            " Internship "
        )

        assert len(results) == 1
        assert results[0].application_type == "Internship"


def test_application_service_upcoming_deadlines_returns_empty_for_invalid_limit():
    setup_database()

    with SessionLocal() as session:
        application_service = ApplicationService(session)

        results = application_service.get_upcoming_deadlines(
            today=date(2026, 8, 1),
            limit=0,
        )

        assert results == []


def test_application_service_gets_sorted_applications():
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
            date_applied=date(2026, 8, 5),
            status="Applied",
        )

        application_service.create_application(
            company_id=company.id,
            position="Software Engineer",
            application_type="Full-time",
            date_applied=date(2026, 8, 4),
            status="Interview",
        )

        results = application_service.get_sorted_applications("date_applied")

        assert len(results) == 2
        assert results[0].date_applied == date(2026, 8, 5)
        assert results[1].date_applied == date(2026, 8, 4)


def test_company_service_rejects_empty_name():
    setup_database()

    with SessionLocal() as session:
        company_service = CompanyService(session)

        with pytest.raises(
            ValueError,
            match="Company name cannot be empty.",
        ):
            company_service.create_company(
                name="   ",
            )


def test_company_service_gets_all_companies():
    setup_database()

    with SessionLocal() as session:
        company_service = CompanyService(session)

        company_service.create_company(
            name="Google",
        )

        company_service.create_company(
            name="Microsoft",
        )

        companies = company_service.get_companies()

        assert len(companies) == 2
        assert companies[0].name == "Google"
        assert companies[1].name == "Microsoft"


def test_company_service_delete_unknown_company():
    setup_database()

    with SessionLocal() as session:
        company_service = CompanyService(session)

        result = company_service.delete_company(9999)

        assert result is False


def test_follow_up_service_gets_follow_up():
    setup_database()

    with SessionLocal() as session:
        company_service = CompanyService(session)
        application_service = ApplicationService(session)
        follow_up_service = FollowUpService(session)

        company = company_service.create_company(
            name="Google",
        )

        application = application_service.create_application(
            company_id=company.id,
            position="Software Engineer",
            application_type="Internship",
            date_applied=date(2026, 8, 20),
            status="Applied",
        )

        follow_up = follow_up_service.create_follow_up(
            FollowUp(
                application_id=application.id,
                follow_up_at=datetime(
                    2026,
                    8,
                    25,
                    10,
                    0,
                    tzinfo=UTC,
                ),
                note="Send follow-up email.",
            )
        )

        result = follow_up_service.get_follow_up(follow_up.id)

        assert result is not None
        assert result.id == follow_up.id
        assert result.application_id == application.id
        assert result.follow_up_at == datetime(
            2026,
            8,
            25,
            10,
            0,
            tzinfo=UTC,
        )
        assert result.note == "Send follow-up email."
        assert result.completed is False


def test_follow_up_service_gets_pending_follow_ups():
    setup_database()

    with SessionLocal() as session:
        company_service = CompanyService(session)
        application_service = ApplicationService(session)
        follow_up_service = FollowUpService(session)

        company = company_service.create_company(
            name="Microsoft",
        )

        application = application_service.create_application(
            company_id=company.id,
            position="Software Engineer",
            application_type="Full-time",
            date_applied=date(2026, 8, 20),
            status="Applied",
        )

        follow_up_service.create_follow_up(
            FollowUp(
                application_id=application.id,
                follow_up_at=datetime(
                    2026,
                    8,
                    25,
                    10,
                    0,
                    tzinfo=UTC,
                ),
                note="Pending follow-up.",
            )
        )

        results = follow_up_service.get_pending_follow_ups()

        assert len(results) == 1
        assert results[0].application_id == application.id
        assert results[0].completed is False
        assert results[0].note == "Pending follow-up."


def test_follow_up_service_gets_completed_follow_ups():
    setup_database()

    with SessionLocal() as session:
        company_service = CompanyService(session)
        application_service = ApplicationService(session)
        follow_up_service = FollowUpService(session)

        company = company_service.create_company(
            name="Amazon",
        )

        application = application_service.create_application(
            company_id=company.id,
            position="Backend Engineer",
            application_type="Internship",
            date_applied=date(2026, 8, 20),
            status="Applied",
        )

        follow_up = follow_up_service.create_follow_up(
            FollowUp(
                application_id=application.id,
                follow_up_at=datetime(
                    2026,
                    8,
                    25,
                    10,
                    0,
                    tzinfo=UTC,
                ),
                note="Completed follow-up.",
            )
        )

        follow_up_service.complete_follow_up(follow_up.id)

        results = follow_up_service.get_completed_follow_ups()

        assert len(results) == 1
        assert results[0].application_id == application.id
        assert results[0].completed is True
        assert results[0].note == "Completed follow-up."


def test_interview_service_analytics_counts_canceled_onsite_passed_and_failed():
    setup_database()

    with SessionLocal() as session:
        company_service = CompanyService(session)
        application_service = ApplicationService(session)
        interview_service = InterviewService(session)

        company = company_service.create_company(
            name="Google",
        )

        application = application_service.create_application(
            company_id=company.id,
            position="Software Engineer",
            application_type="Full-time",
            date_applied=date(2026, 8, 20),
            status="Applied",
        )

        canceled_interview = Interview(
            application_id=application.id,
            scheduled_at=datetime(
                2026,
                8,
                25,
                10,
                0,
                tzinfo=UTC,
            ),
            interview_type=InterviewType.ONLINE,
            status=InterviewStatus.CANCELED,
        )

        onsite_passed_interview = Interview(
            application_id=application.id,
            scheduled_at=datetime(
                2026,
                8,
                26,
                10,
                0,
                tzinfo=UTC,
            ),
            interview_type=InterviewType.ONSITE,
            status=InterviewStatus.COMPLETED,
            outcome=InterviewOutcome.PASSED,
        )

        onsite_failed_interview = Interview(
            application_id=application.id,
            scheduled_at=datetime(
                2026,
                8,
                27,
                10,
                0,
                tzinfo=UTC,
            ),
            interview_type=InterviewType.ONSITE,
            status=InterviewStatus.COMPLETED,
            outcome=InterviewOutcome.FAILED,
        )

        interview_service.create_interview(canceled_interview)

        interview_service.create_interview(onsite_passed_interview)

        interview_service.create_interview(onsite_failed_interview)

        analytics = interview_service.get_interview_analytics()

        assert analytics["total"] == 3
        assert analytics["cancelled"] == 1
        assert analytics["on_site"] == 2
        assert analytics["passed"] == 1
        assert analytics["failed"] == 1
        assert analytics["pending"] == 1


def test_import_service_raises_file_not_found_error():
    setup_database()

    with SessionLocal() as session:
        application_service = ApplicationService(session)

        import_service = ImportService(application_service)

        with pytest.raises(FileNotFoundError):
            import_service.import_applications_from_csv("nonexistent_file.csv")
