import csv
from datetime import date

from app.database.connection import Base, SessionLocal, engine
from app.database.init_db import initialize_database
from app.database.models.application import ApplicationDB
from app.database.models.company import CompanyDB
from app.services.application_service import ApplicationService
from app.services.export_service import ExportService


def setup_database():
    Base.metadata.drop_all(bind=engine)
    initialize_database()


def test_export_applications_to_csv(
    tmp_path,
    monkeypatch,
):
    setup_database()

    with SessionLocal() as session:
        company = CompanyDB(
            name="Microsoft",
        )

        session.add(company)
        session.commit()
        session.refresh(company)

        application = ApplicationDB(
            company_id=company.id,
            position="Software Engineer",
            application_type="Full-time",
            date_applied=date(2026, 7, 10),
            status="Applied",
            location="Addis Ababa",
            deadline=date(2026, 8, 20),
            job_url="https://example.com/job",
            notes="Follow up after one week.",
        )

        session.add(application)
        session.commit()

        application_service = ApplicationService(
            session
        )

        exporter = ExportService(
            application_service
        )

        monkeypatch.chdir(tmp_path)

        export_path = (
            exporter.export_applications_to_csv()
        )

        with open(
            export_path,
            newline="",
            encoding="utf-8",
        ) as file:
            rows = list(csv.reader(file))

    assert rows[0] == [
        "Company",
        "Position",
        "Application Type",
        "Status",
        "Date Applied",
        "Location",
        "Deadline",
        "Job URL",
        "Notes",
    ]

    assert rows[1] == [
        "Microsoft",
        "Software Engineer",
        "Full-time",
        "Applied",
        "2026-07-10",
        "Addis Ababa",
        "2026-08-20",
        "https://example.com/job",
        "Follow up after one week.",
    ]