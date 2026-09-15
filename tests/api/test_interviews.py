from datetime import datetime, timezone

import pytest
from fastapi.testclient import TestClient

from app.api.dependencies import get_db
from app.api.main import app
from app.database.models.application import ApplicationDB
from app.database.models.company import CompanyDB
from app.database.models.interview import InterviewDB


def get_client(db_session):
    app.dependency_overrides[get_db] = lambda: db_session
    return TestClient(app)


def create_application(db_session):
    company = CompanyDB(
        name="Microsoft",
        website="https://www.microsoft.com/",
        industry="Technology",
        location="Redmond, WA",
    )

    db_session.add(company)
    db_session.commit()
    db_session.refresh(company)

    application = ApplicationDB(
        company_id=company.id,
        position="Software Engineering Intern",
        application_type="Internship",
        date_applied=datetime(2026, 9, 5).date(),
        status="Applied",
    )

    db_session.add(application)
    db_session.commit()
    db_session.refresh(application)

    return application


def test_create_interview(db_session):
    application = create_application(db_session)

    client = get_client(db_session)

    response = client.post(
        "/api/interviews",
        json={
            "application_id": application.id,
            "scheduled_at": "2026-09-15T10:00:00Z",
            "interview_type": "Online",
            "status": "Scheduled",
            "outcome": "Pending",
            "notes": "Technical interview",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["id"] == 1
    assert data["application_id"] == application.id
    assert data["interview_type"] == "Online"
    assert data["status"] == "Scheduled"
    assert data["outcome"] == "Pending"
    assert data["notes"] == "Technical interview"


def test_get_interviews(db_session):
    application = create_application(db_session)

    interview = InterviewDB(
        application_id=application.id,
        scheduled_at=datetime(
            2026,
            9,
            15,
            10,
            0,
            tzinfo=timezone.utc,
        ),
        interview_type="Online",
        status="Scheduled",
        outcome="Pending",
        notes="Technical interview",
    )

    db_session.add(interview)
    db_session.commit()

    client = get_client(db_session)

    response = client.get("/api/interviews")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["id"] == 1
    assert data[0]["application_id"] == application.id
    assert data[0]["interview_type"] == "Online"


def test_get_interview(db_session):
    application = create_application(db_session)

    interview = InterviewDB(
        application_id=application.id,
        scheduled_at=datetime(
            2026,
            9,
            15,
            10,
            0,
            tzinfo=timezone.utc,
        ),
        interview_type="Online",
        status="Scheduled",
        outcome="Pending",
    )

    db_session.add(interview)
    db_session.commit()

    client = get_client(db_session)

    response = client.get("/api/interviews/1")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == 1
    assert data["application_id"] == application.id
    assert data["interview_type"] == "Online"
    assert data["status"] == "Scheduled"


def test_get_interview_not_found(db_session):
    client = get_client(db_session)

    response = client.get("/api/interviews/999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Interview not found."
    }


def test_update_interview(db_session):
    application = create_application(db_session)

    interview = InterviewDB(
        application_id=application.id,
        scheduled_at=datetime(
            2026,
            9,
            15,
            10,
            0,
            tzinfo=timezone.utc,
        ),
        interview_type="Online",
        status="Scheduled",
        outcome="Pending",
        notes="Original notes",
    )

    db_session.add(interview)
    db_session.commit()

    client = get_client(db_session)

    response = client.put(
        "/api/interviews/1",
        json={
            "status": "Completed",
            "outcome": "Passed",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == 1
    assert data["status"] == "Completed"
    assert data["outcome"] == "Passed"
    assert data["notes"] == "Original notes"


def test_update_interview_not_found(db_session):
    client = get_client(db_session)

    response = client.put(
        "/api/interviews/999",
        json={
            "status": "Completed",
            "outcome": "Passed",
        },
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Interview not found."
    }


def test_delete_interview(db_session):
    application = create_application(db_session)

    interview = InterviewDB(
        application_id=application.id,
        scheduled_at=datetime(
            2026,
            9,
            15,
            10,
            0,
            tzinfo=timezone.utc,
        ),
        interview_type="Online",
        status="Scheduled",
        outcome="Pending",
    )

    db_session.add(interview)
    db_session.commit()

    client = get_client(db_session)

    response = client.delete("/api/interviews/1")

    assert response.status_code == 204
    assert db_session.get(InterviewDB, 1) is None


def test_delete_interview_not_found(db_session):
    client = get_client(db_session)

    response = client.delete("/api/interviews/999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Interview not found."
    }


@pytest.fixture(autouse=True)
def clear_dependency_overrides():
    yield
    app.dependency_overrides.clear()
