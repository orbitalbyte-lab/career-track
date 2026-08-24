from datetime import date

from app.database.connection import Base, SessionLocal, engine
from app.database.init_db import initialize_database
from app.database.models.application import ApplicationDB
from app.database.models.company import CompanyDB
from app.repositories.application_repository import ApplicationRepository
from app.repositories.company_repository import CompanyRepository


def setup_database():
    Base.metadata.drop_all(bind=engine)
    initialize_database()


def test_company_repository_create_and_get():
    setup_database()

    with SessionLocal() as session:
        repository = CompanyRepository(session)

        company = CompanyDB(
            name="Microsoft",
            industry="Technology",
        )

        created_company = repository.create(company)

        assert created_company.id is not None

        found_company = repository.get_by_id(created_company.id)

        assert found_company is not None
        assert found_company.name == "Microsoft"


def test_application_repository_create_and_get_by_company():
    setup_database()

    with SessionLocal() as session:
        company_repository = CompanyRepository(session)
        application_repository = ApplicationRepository(session)

        company = company_repository.create(
            CompanyDB(
                name="Google",
                industry="Technology",
            )
        )

        application = ApplicationDB(
            company_id=company.id,
            position="Software Engineering Intern",
            application_type="Internship",
            date_applied=date(2026, 7, 30),
            status="Applied",
        )

        created_application = application_repository.create(application)

        assert created_application.id is not None

        applications = application_repository.get_by_company_id(
            company.id
        )

        assert len(applications) == 1
        assert applications[0].position == "Software Engineering Intern"


def test_company_repository_get_all():
    setup_database()

    with SessionLocal() as session:
        repository = CompanyRepository(session)

        repository.create(CompanyDB(name="Microsoft"))
        repository.create(CompanyDB(name="Google"))

        companies = repository.get_all()

        assert len(companies) == 2


def test_application_repository_get_all():
    setup_database()

    with SessionLocal() as session:
        company = CompanyRepository(session).create(
            CompanyDB(name="Microsoft")
        )

        repository = ApplicationRepository(session)

        repository.create(
            ApplicationDB(
                company_id=company.id,
                position="Software Engineer",
                application_type="Full-time",
                date_applied=date(2026, 7, 30),
                status="Applied",
            )
        )

        applications = repository.get_all()

        assert len(applications) == 1


def test_company_repository_searches_by_name():
    setup_database()

    with SessionLocal() as session:
        repository = CompanyRepository(session)

        repository.create(
            CompanyDB(
                name="Microsoft",
                industry="Technology",
            )
        )

        repository.create(
            CompanyDB(
                name="Google",
                industry="Technology",
            )
        )

        repository.create(
            CompanyDB(
                name="Amazon",
                industry="Technology",
            )
        )

        results = repository.search("micro")

        assert len(results) == 1
        assert results[0].name == "Microsoft"


def test_company_repository_search_orders_by_name():
    setup_database()

    with SessionLocal() as session:
        repository = CompanyRepository(session)

        repository.create(CompanyDB(name="Microsoft"))
        repository.create(CompanyDB(name="Apple"))
        repository.create(CompanyDB(name="Google"))

        results = repository.search("")

        assert [company.name for company in results] == [
            "Apple",
            "Google",
            "Microsoft",
        ]


def test_application_repository_searches_by_position():
    setup_database()

    with SessionLocal() as session:
        company_repository = CompanyRepository(session)
        application_repository = ApplicationRepository(session)

        company = company_repository.create(
            CompanyDB(name="Google")
        )

        application_repository.create(
            ApplicationDB(
                company_id=company.id,
                position="Software Engineering Intern",
                application_type="Internship",
                date_applied=date(2026, 8, 4),
                status="Applied",
            )
        )

        application_repository.create(
            ApplicationDB(
                company_id=company.id,
                position="Data Analyst Intern",
                application_type="Internship",
                date_applied=date(2026, 8, 4),
                status="Applied",
            )
        )

        results = application_repository.search("engineering")

        assert len(results) == 1
        assert results[0].position == "Software Engineering Intern"


def test_application_repository_search_orders_by_position():
    setup_database()

    with SessionLocal() as session:
        company_repository = CompanyRepository(session)
        application_repository = ApplicationRepository(session)

        company = company_repository.create(
            CompanyDB(name="Google")
        )

        application_repository.create(
            ApplicationDB(
                company_id=company.id,
                position="Software Engineer",
                application_type="Full-time",
                date_applied=date(2026, 8, 4),
                status="Applied",
            )
        )

        application_repository.create(
            ApplicationDB(
                company_id=company.id,
                position="Backend Engineer",
                application_type="Full-time",
                date_applied=date(2026, 8, 4),
                status="Applied",
            )
        )

        application_repository.create(
            ApplicationDB(
                company_id=company.id,
                position="Data Analyst",
                application_type="Full-time",
                date_applied=date(2026, 8, 4),
                status="Applied",
            )
        )

        results = application_repository.search("")

        assert [application.position for application in results] == [
            "Backend Engineer",
            "Data Analyst",
            "Software Engineer",
        ]


def test_application_repository_searches_by_company_name():
    setup_database()

    with SessionLocal() as session:
        company_repository = CompanyRepository(session)
        application_repository = ApplicationRepository(session)

        google = company_repository.create(
            CompanyDB(name="Google")
        )

        microsoft = company_repository.create(
            CompanyDB(name="Microsoft")
        )

        application_repository.create(
            ApplicationDB(
                company_id=google.id,
                position="Software Engineering Intern",
                application_type="Internship",
                date_applied=date(2026, 8, 4),
                status="Applied",
            )
        )

        application_repository.create(
            ApplicationDB(
                company_id=microsoft.id,
                position="Data Analyst Intern",
                application_type="Internship",
                date_applied=date(2026, 8, 4),
                status="Applied",
            )
        )

        results = application_repository.search("google")

        assert len(results) == 1
        assert results[0].company.name == "Google"
        assert results[0].position == "Software Engineering Intern"


def test_application_repository_searches_by_position_or_company_name():
    setup_database()

    with SessionLocal() as session:
        company_repository = CompanyRepository(session)
        application_repository = ApplicationRepository(session)

        google = company_repository.create(
            CompanyDB(name="Google")
        )

        microsoft = company_repository.create(
            CompanyDB(name="Microsoft")
        )

        application_repository.create(
            ApplicationDB(
                company_id=google.id,
                position="Software Engineering Intern",
                application_type="Internship",
                date_applied=date(2026, 8, 4),
                status="Applied",
            )
        )

        application_repository.create(
            ApplicationDB(
                company_id=microsoft.id,
                position="Data Analyst Intern",
                application_type="Internship",
                date_applied=date(2026, 8, 4),
                status="Applied",
            )
        )

        results = application_repository.search("engineering")

        assert len(results) == 1
        assert results[0].position == "Software Engineering Intern"

        results = application_repository.search("microsoft")

        assert len(results) == 1
        assert results[0].company.name == "Microsoft"


def test_application_repository_searches_by_status():
    setup_database()

    with SessionLocal() as session:
        company_repository = CompanyRepository(session)
        application_repository = ApplicationRepository(session)

        company = company_repository.create(
            CompanyDB(name="Google")
        )

        application_repository.create(
            ApplicationDB(
                company_id=company.id,
                position="Software Engineer",
                application_type="Full-time",
                date_applied=date(2026, 8, 4),
                status="Interview",
            )
        )

        application_repository.create(
            ApplicationDB(
                company_id=company.id,
                position="Data Analyst",
                application_type="Internship",
                date_applied=date(2026, 8, 4),
                status="Applied",
            )
        )

        results = application_repository.search("interview")

        assert len(results) == 1
        assert results[0].status == "Interview"
        assert results[0].position == "Software Engineer"


def test_application_repository_searches_by_application_type():
    setup_database()

    with SessionLocal() as session:
        company_repository = CompanyRepository(session)
        application_repository = ApplicationRepository(session)

        company = company_repository.create(
            CompanyDB(name="Microsoft")
        )

        application_repository.create(
            ApplicationDB(
                company_id=company.id,
                position="Software Engineer",
                application_type="Full-time",
                date_applied=date(2026, 8, 4),
                status="Applied",
            )
        )

        application_repository.create(
            ApplicationDB(
                company_id=company.id,
                position="Software Engineering Intern",
                application_type="Internship",
                date_applied=date(2026, 8, 4),
                status="Applied",
            )
        )

        results = application_repository.search("internship")

        assert len(results) == 1
        assert results[0].application_type == "Internship"
        assert results[0].position == "Software Engineering Intern"


def test_application_repository_filters_by_status():
    setup_database()

    with SessionLocal() as session:
        company_repository = CompanyRepository(session)
        application_repository = ApplicationRepository(session)

        company = company_repository.create(
            CompanyDB(name="Google")
        )

        application_repository.create(
            ApplicationDB(
                company_id=company.id,
                position="Software Engineer",
                application_type="Full-time",
                date_applied=date(2026, 8, 4),
                status="Applied",
            )
        )

        application_repository.create(
            ApplicationDB(
                company_id=company.id,
                position="Backend Engineer",
                application_type="Full-time",
                date_applied=date(2026, 8, 4),
                status="Interview",
            )
        )

        application_repository.create(
            ApplicationDB(
                company_id=company.id,
                position="Data Analyst",
                application_type="Internship",
                date_applied=date(2026, 8, 4),
                status="Rejected",
            )
        )

        results = application_repository.get_by_status("Interview")

        assert len(results) == 1
        assert results[0].position == "Backend Engineer"
        assert results[0].status == "Interview"


def test_application_repository_filters_by_application_type():
    setup_database()

    with SessionLocal() as session:
        company_repository = CompanyRepository(session)
        application_repository = ApplicationRepository(session)

        company = company_repository.create(
            CompanyDB(name="Microsoft")
        )

        application_repository.create(
            ApplicationDB(
                company_id=company.id,
                position="Software Engineer",
                application_type="Full-time",
                date_applied=date(2026, 8, 4),
                status="Applied",
            )
        )

        application_repository.create(
            ApplicationDB(
                company_id=company.id,
                position="Software Engineering Intern",
                application_type="Internship",
                date_applied=date(2026, 8, 4),
                status="Applied",
            )
        )

        application_repository.create(
            ApplicationDB(
                company_id=company.id,
                position="Backend Intern",
                application_type="Internship",
                date_applied=date(2026, 8, 4),
                status="Interview",
            )
        )

        results = application_repository.get_by_application_type(
            "Internship"
        )

        assert len(results) == 2
        assert results[0].application_type == "Internship"
        assert results[1].application_type == "Internship"

def test_application_repository_filters_by_date():
    setup_database()

    with SessionLocal() as session:
        company_repository = CompanyRepository(session)
        application_repository = ApplicationRepository(session)

        company = company_repository.create(
            CompanyDB(name="Google")
        )

        application_repository.create(
            ApplicationDB(
                company_id=company.id,
                position="Backend Engineer",
                application_type="Full-time",
                date_applied=date(2026, 8, 4),
                status="Applied",
            )
        )

        application_repository.create(
            ApplicationDB(
                company_id=company.id,
                position="Software Engineer",
                application_type="Full-time",
                date_applied=date(2026, 8, 5),
                status="Interview",
            )
        )

        results = application_repository.get_by_date(
            date(2026, 8, 4)
        )

        assert len(results) == 1
        assert results[0].position == "Backend Engineer"
        assert results[0].date_applied == date(2026, 8, 4)

def test_application_repository_filters_by_deadline():
    setup_database()

    with SessionLocal() as session:
        company_repository = CompanyRepository(session)
        application_repository = ApplicationRepository(session)

        company = company_repository.create(
            CompanyDB(name="Google")
        )

        application_repository.create(
            ApplicationDB(
                company_id=company.id,
                position="Backend Engineer",
                application_type="Full-time",
                date_applied=date(2026, 8, 4),
                deadline=date(2026, 8, 20),
                status="Applied",
            )
        )

        application_repository.create(
            ApplicationDB(
                company_id=company.id,
                position="Software Engineer",
                application_type="Full-time",
                date_applied=date(2026, 8, 5),
                deadline=date(2026, 8, 25),
                status="Interview",
            )
        )

        results = application_repository.get_by_deadline(
            date(2026, 8, 20)
        )

        assert len(results) == 1
        assert results[0].position == "Backend Engineer"
        assert results[0].deadline == date(2026, 8, 20)

def test_application_repository_sorts_by_date_applied_descending():
    setup_database()

    with SessionLocal() as session:
        company_repository = CompanyRepository(session)
        application_repository = ApplicationRepository(session)

        company = company_repository.create(
            CompanyDB(name="Google")
        )

        application_repository.create(
            ApplicationDB(
                company_id=company.id,
                position="Old Application",
                application_type="Full-time",
                date_applied=date(2026, 8, 1),
                status="Applied",
            )
        )

        application_repository.create(
            ApplicationDB(
                company_id=company.id,
                position="New Application",
                application_type="Full-time",
                date_applied=date(2026, 8, 5),
                status="Applied",
            )
        )

        results = application_repository.get_all_sorted_by_date()

        assert len(results) == 2
        assert results[0].position == "New Application"
        assert results[1].position == "Old Application"
def test_application_repository_sorts_by_date_field():
    setup_database()

    with SessionLocal() as session:
        company_repository = CompanyRepository(session)
        application_repository = ApplicationRepository(session)

        company = company_repository.create(
            CompanyDB(name="Google")
        )

        application_repository.create(
            ApplicationDB(
                company_id=company.id,
                position="Old Application",
                application_type="Full-time",
                date_applied=date(2026, 8, 1),
                status="Applied",
            )
        )

        application_repository.create(
            ApplicationDB(
                company_id=company.id,
                position="New Application",
                application_type="Full-time",
                date_applied=date(2026, 8, 5),
                status="Applied",
            )
        )

        results = application_repository.get_all_sorted(
            "date"
        )

        assert len(results) == 2
        assert results[0].position == "New Application"
        assert results[1].position == "Old Application"


def test_application_repository_sorts_by_position():
    setup_database()

    with SessionLocal() as session:
        company_repository = CompanyRepository(session)
        application_repository = ApplicationRepository(session)

        company = company_repository.create(
            CompanyDB(name="Google")
        )

        application_repository.create(
            ApplicationDB(
                company_id=company.id,
                position="Software Engineer",
                application_type="Full-time",
                date_applied=date(2026, 8, 5),
                status="Applied",
            )
        )

        application_repository.create(
            ApplicationDB(
                company_id=company.id,
                position="Backend Engineer",
                application_type="Full-time",
                date_applied=date(2026, 8, 4),
                status="Applied",
            )
        )

        application_repository.create(
            ApplicationDB(
                company_id=company.id,
                position="Frontend Engineer",
                application_type="Internship",
                date_applied=date(2026, 8, 3),
                status="Applied",
            )
        )

        results = application_repository.get_all_sorted(
            "position"
        )
        assert len(results) == 3
        assert results[0].position == "Backend Engineer"
        assert results[1].position == "Frontend Engineer"
        assert results[2].position == "Software Engineer"
def test_get_monthly_application_counts():
    setup_database()

    with SessionLocal() as session:
        company = CompanyRepository(session).create(
             CompanyDB(name="Microsoft")
        )
        repository = ApplicationRepository(session)

        repository.create(
            ApplicationDB(
                company_id=company.id,
                position="Software Engineer",
                application_type="Full-time",
                date_applied=date(2026, 7, 10),
                status="Applied",
            )
        )

        repository.create(
            ApplicationDB(
                company_id=company.id,
                position="Backend Engineer",
                application_type="Full-time",
                date_applied=date(2026, 7, 20),
                status="Interview",
            )
        )

        repository.create(
            ApplicationDB(
                company_id=company.id,
                position="Frontend Engineer",
                application_type="Internship",
                date_applied=date(2026, 8, 5),
                status="Applied",
            )
        )

        result = repository.get_monthly_application_counts()

        assert result == {
            "2026-07": 2,
            "2026-08": 1,
        }

def test_get_location_statistics():
    setup_database()

    with SessionLocal() as session:
        company = CompanyRepository(session).create(
            CompanyDB(name="Microsoft")
        )

        repository = ApplicationRepository(session)

        repository.create(
            ApplicationDB(
                company_id=company.id,
                position="Software Engineer",
                application_type="Full-time",
                date_applied=date(2026, 7, 10),
                status="Applied",
                location="Remote",
            )
        )

        repository.create(
            ApplicationDB(
                company_id=company.id,
                position="Backend Engineer",
                application_type="Full-time",
                date_applied=date(2026, 7, 20),
                status="Interview",
                location="Remote",
            )
        )

        repository.create(
            ApplicationDB(
                company_id=company.id,
                position="Frontend Engineer",
                application_type="Internship",
                date_applied=date(2026, 8, 5),
                status="Applied",
                location="Addis Ababa",
            )
        )

        repository.create(
            ApplicationDB(
                company_id=company.id,
                position="Data Analyst",
                application_type="Internship",
                date_applied=date(2026, 8, 8),
                status="Applied",
            )
        )

        result = repository.get_location_statistics()

        assert result == {
            "Remote": 2,
            "Addis Ababa": 1,
            "Not specified": 1,
        }
