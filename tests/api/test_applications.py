from datetime import date

import pytest
from fastapi.testclient import TestClient

from app.api.dependencies import get_db
from app.api.main import app
from app.database.models.application import ApplicationDB
from app.database.models.company import CompanyDB


def get_client(db_session):
    app.dependency_overrides[get_db] = lambda: db_session
    return TestClient(app)


def create_company(db_session):
    company = CompanyDB(
        name="Microsoft",
        website="https://www.microsoft.com/",
        industry="Technology",
        location="Redmond, WA",
    )

    db_session.add(company)
    db_session.commit()
    db_session.refresh(company)

    return company


def test_create_application(db_session):
    company = create_company(db_session)

    client = get_client(db_session)

    response = client.post(
        "/api/applications",
        json={
            "company_id": company.id,
            "position": "Software Engineering Intern",
            "application_type": "Internship",
            "date_applied": "2026-09-05",
            "status": "Applied",
            "location": "Redmond, WA",
            "deadline": None,
            "job_url": "https://www.microsoft.com/",
            "notes": "Testing Applications API",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["id"] == 1
    assert data["company_id"] == company.id
    assert data["position"] == "Software Engineering Intern"
    assert data["application_type"] == "Internship"
    assert data["status"] == "Applied"

def test_create_application_rejects_deadline_before_application_date(
    db_session,
):
    company = create_company(db_session)

    client = get_client(db_session)

    response = client.post(
        "/api/applications",
        json={
            "company_id": company.id,
            "position": "Software Engineering Intern",
            "application_type": "Internship",
            "date_applied": "2026-08-10",
            "status": "Applied",
            "deadline": "2026-08-05",
        },
    )

    assert response.status_code == 422
    assert "Deadline cannot be before the application date." in str(
        response.json()
    )

def test_create_application_company_not_found(db_session):
    client = get_client(db_session)

    response = client.post(
        "/api/applications",
        json={
            "company_id": 999,
            "position": "Software Engineering Intern",
            "application_type": "Internship",
            "date_applied": "2026-09-05",
            "status": "Applied",
        },
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "Company not found"
    }


def test_get_applications(db_session):
    company = create_company(db_session)

    application = ApplicationDB(
        company_id=company.id,
        position="Software Engineering Intern",
        application_type="Internship",
        date_applied=date(2026, 9, 5),
        status="Applied",
        location="Redmond, WA",
        job_url="https://www.microsoft.com/",
    )

    db_session.add(application)
    db_session.commit()

    client = get_client(db_session)

    response = client.get("/api/applications")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["id"] == 1
    assert data[0]["company_id"] == company.id
    assert data[0]["position"] == "Software Engineering Intern"


def test_get_applications_pagination(db_session):
    company = create_company(db_session)

    applications = [
        ApplicationDB(
            company_id=company.id,
            position=f"Position {index}",
            application_type="Internship",
            date_applied=date(2026, 8, index),
            status="Applied",
        )
        for index in range(1, 26)
    ]

    db_session.add_all(applications)
    db_session.commit()

    client = get_client(db_session)

    response = client.get(
        "/api/applications?page=2&page_size=10"
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 10
    assert data[0]["position"] == "Position 15"
    assert data[-1]["position"] == "Position 6"


def test_get_applications_pagination_last_page(db_session):
    company = create_company(db_session)

    applications = [
        ApplicationDB(
            company_id=company.id,
            position=f"Position {index}",
            application_type="Internship",
            date_applied=date(2026, 8, index),
            status="Applied",
        )
        for index in range(1, 26)
    ]

    db_session.add_all(applications)
    db_session.commit()

    client = get_client(db_session)

    response = client.get(
        "/api/applications?page=3&page_size=10"
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 5
    assert data[0]["position"] == "Position 5"
    assert data[-1]["position"] == "Position 1"


def test_get_applications_rejects_invalid_page(db_session):
    client = get_client(db_session)

    response = client.get(
        "/api/applications?page=0"
    )

    assert response.status_code == 422


def test_get_applications_rejects_invalid_page_size(db_session):
    client = get_client(db_session)

    response = client.get(
        "/api/applications?page_size=0"
    )

    assert response.status_code == 422


def test_get_applications_rejects_page_size_over_100(db_session):
    client = get_client(db_session)

    response = client.get(
        "/api/applications?page_size=101"
    )

    assert response.status_code == 422


def test_get_application(db_session):
    company = create_company(db_session)

    application = ApplicationDB(
        company_id=company.id,
        position="Software Engineering Intern",
        application_type="Internship",
        date_applied=date(2026, 9, 5),
        status="Applied",
    )

    db_session.add(application)
    db_session.commit()

    client = get_client(db_session)

    response = client.get("/api/applications/1")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == 1
    assert data["company_id"] == company.id
    assert data["position"] == "Software Engineering Intern"


def test_get_application_not_found(db_session):
    client = get_client(db_session)

    response = client.get("/api/applications/999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Application not found."
    }


def test_update_application(db_session):
    company = create_company(db_session)

    application = ApplicationDB(
        company_id=company.id,
        position="Software Engineering Intern",
        application_type="Internship",
        date_applied=date(2026, 9, 5),
        status="Applied",
        location="Redmond, WA",
        notes="Original notes",
    )

    db_session.add(application)
    db_session.commit()

    client = get_client(db_session)

    response = client.put(
        "/api/applications/1",
        json={
            "position": "Software Engineer Intern",
            "application_type": "Internship",
            "date_applied": "2026-09-05",
            "status": "Under Review",
            "location": "Redmond, Washington",
            "deadline": None,
            "job_url": "https://www.microsoft.com/",
            "notes": "Updated through API tests",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == 1
    assert data["position"] == "Software Engineer Intern"
    assert data["status"] == "Under Review"
    assert data["location"] == "Redmond, Washington"
    assert data["notes"] == "Updated through API tests"


def test_update_application_not_found(db_session):
    client = get_client(db_session)

    response = client.put(
        "/api/applications/999",
        json={
            "position": "Software Engineer Intern",
        },
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Application not found."
    }


def test_delete_application(db_session):
    company = create_company(db_session)

    application = ApplicationDB(
        company_id=company.id,
        position="Software Engineering Intern",
        application_type="Internship",
        date_applied=date(2026, 9, 5),
        status="Applied",
    )

    db_session.add(application)
    db_session.commit()

    client = get_client(db_session)

    response = client.delete("/api/applications/1")

    assert response.status_code == 204
    assert db_session.get(ApplicationDB, 1) is None


def test_delete_application_not_found(db_session):
    client = get_client(db_session)

    response = client.delete("/api/applications/999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Application not found."
    }


@pytest.fixture(autouse=True)
def clear_dependency_overrides():
    yield
    app.dependency_overrides.clear()