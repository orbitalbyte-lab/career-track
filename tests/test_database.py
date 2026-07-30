from datetime import date

from sqlalchemy import inspect, text

from app.database.connection import Base, SessionLocal, engine
from app.database.init_db import initialize_database
from app.database.models.application import ApplicationDB
from app.database.models.company import CompanyDB


def test_database_connection():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))

        assert result.scalar() == 1


def test_company_table_is_created():
    initialize_database()

    inspector = inspect(engine)

    assert "companies" in inspector.get_table_names()


def test_application_table_is_created():
    initialize_database()

    inspector = inspect(engine)

    assert "applications" in inspector.get_table_names()


def test_application_has_company_foreign_key():
    initialize_database()

    inspector = inspect(engine)

    foreign_keys = inspector.get_foreign_keys("applications")

    assert any(
        foreign_key["referred_table"] == "companies"
        for foreign_key in foreign_keys
    )


def test_application_can_be_saved_with_company():
    Base.metadata.drop_all(bind=engine)
    initialize_database()

    with SessionLocal() as session:
        company = CompanyDB(
            name="Microsoft",
            industry="Technology",
        )

        application = ApplicationDB(
            company=company,
            position="Software Engineering Intern",
            application_type="Internship",
            date_applied=date(2026, 7, 30),
            status="Applied",
        )

        session.add(application)
        session.commit()

        assert application.id is not None
        assert company.id is not None
        assert application.company_id == company.id