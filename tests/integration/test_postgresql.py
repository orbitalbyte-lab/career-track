import os

import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from app.database.models import CompanyDB


DATABASE_URL = os.getenv("DATABASE_URL")


@pytest.fixture
def postgres_session():
    if not DATABASE_URL or not DATABASE_URL.startswith("postgresql"):
        pytest.skip("PostgreSQL DATABASE_URL is not configured.")

    engine = create_engine(
        DATABASE_URL,
        echo=False,
    )

    SessionLocal = sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False,
    )

    with SessionLocal() as session:
        yield session

    engine.dispose()


def test_postgresql_connection(postgres_session):
    result = postgres_session.execute(
        text("SELECT 1")
    ).scalar_one()

    assert result == 1


def test_postgresql_tables_exist(postgres_session):
    result = postgres_session.execute(
        text(
            """
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
            AND table_name IN (
                'companies',
                'applications',
                'interviews',
                'follow_ups'
            )
            ORDER BY table_name
            """
        )
    ).scalars().all()

    assert result == [
        "applications",
        "companies",
        "follow_ups",
        "interviews",
    ]


def test_postgresql_company_crud(postgres_session):
    company = CompanyDB(
        name="PostgreSQL Integration Test",
        website="https://example.com",
        notes="Temporary integration test company",
    )

    postgres_session.add(company)
    postgres_session.commit()
    postgres_session.refresh(company)

    assert company.id is not None
    assert company.name == "PostgreSQL Integration Test"

    saved_company = postgres_session.get(
        CompanyDB,
        company.id,
    )

    assert saved_company is not None
    assert saved_company.name == "PostgreSQL Integration Test"

    postgres_session.delete(saved_company)
    postgres_session.commit()

    deleted_company = postgres_session.get(
        CompanyDB,
        company.id,
    )

    assert deleted_company is None