from datetime import datetime, timezone

import pytest
from fastapi.testclient import TestClient

from app.api.dependencies import get_db
from app.api.main import app
from app.database.models.application import ApplicationDB
from app.database.models.company import CompanyDB
from app.database.models.interview import InterviewDB
from app.database.models.user import UserDB
from app.security.jwt import create_access_token
TEST_SECRET_KEY = (
    "test-secret-key-for-interviews-hs256-with-32-bytes-minimum"
)

def get_client(db_session):
    app.dependency_overrides[get_db] = lambda: db_session

    user = UserDB(
        email="interview-user@example.com",
        password_hash="test-hash",
        is_active=True,
    )

    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    token = create_access_token(str(user.id))

    client = TestClient(app)

    client.headers.update(
        {
            "Authorization": f"Bearer {token}",
        }
    )

    return client
def get_unauthenticated_client(db_session):
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

def test_create_interview_requires_authentication(
    db_session,
):
    client = get_unauthenticated_client(db_session)

    response = client.post(
        "/api/interviews",
        json={
            "application_id": 999,
            "scheduled_at": "2026-09-15T10:00:00Z",
            "interview_type": "Online",
            "status": "Scheduled",
            "outcome": "Pending",
            "notes": "Technical interview",
        },
    )

    assert response.status_code == 401
    assert response.headers["WWW-Authenticate"] == "Bearer"
    assert response.json() == {
        "detail": "Could not validate credentials."
    }

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

def test_create_interview_rejects_invalid_application_id(db_session):
    client = get_client(db_session)

    response = client.post(
        "/api/interviews",
        json={
            "application_id": 0,
            "scheduled_at": "2026-09-15T10:00:00Z",
            "interview_type": "Online",
        },
    )

    assert response.status_code == 422


def test_create_interview_rejects_naive_datetime(db_session):
    application = create_application(db_session)

    client = get_client(db_session)

    response = client.post(
        "/api/interviews",
        json={
            "application_id": application.id,
            "scheduled_at": "2026-09-15T10:00:00",
            "interview_type": "Online",
        },
    )

    assert response.status_code == 422
    assert "Scheduled time must include a timezone." in str(
        response.json()
    )


def test_create_interview_rejects_long_notes(db_session):
    application = create_application(db_session)

    client = get_client(db_session)

    response = client.post(
        "/api/interviews",
        json={
            "application_id": application.id,
            "scheduled_at": "2026-09-15T10:00:00Z",
            "interview_type": "Online",
            "notes": "x" * 2001,
        },
    )

    assert response.status_code == 422

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


def test_get_interviews_pagination(db_session):
    application = create_application(db_session)

    interviews = [
        InterviewDB(
            application_id=application.id,
            scheduled_at=datetime(
                2026,
                8,
                index,
                10,
                0,
                tzinfo=timezone.utc,
            ),
            interview_type="Online",
            status="Scheduled",
            outcome="Pending",
        )
        for index in range(1, 26)
    ]

    db_session.add_all(interviews)
    db_session.commit()

    client = get_client(db_session)

    response = client.get(
        "/api/interviews?page=2&page_size=10"
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 10
    assert data[0]["scheduled_at"].startswith("2026-08-11")
    assert data[-1]["scheduled_at"].startswith("2026-08-20")


def test_get_interviews_pagination_last_page(db_session):
    application = create_application(db_session)

    interviews = [
        InterviewDB(
            application_id=application.id,
            scheduled_at=datetime(
                2026,
                8,
                index,
                10,
                0,
                tzinfo=timezone.utc,
            ),
            interview_type="Online",
            status="Scheduled",
            outcome="Pending",
        )
        for index in range(1, 26)
    ]

    db_session.add_all(interviews)
    db_session.commit()

    client = get_client(db_session)

    response = client.get(
        "/api/interviews?page=3&page_size=10"
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 5
    assert data[0]["scheduled_at"].startswith("2026-08-21")
    assert data[-1]["scheduled_at"].startswith("2026-08-25")


def test_get_interviews_rejects_invalid_page(db_session):
    client = get_client(db_session)

    response = client.get(
        "/api/interviews?page=0"
    )

    assert response.status_code == 422


def test_get_interviews_rejects_invalid_page_size(db_session):
    client = get_client(db_session)

    response = client.get(
        "/api/interviews?page_size=0"
    )

    assert response.status_code == 422


def test_get_interviews_rejects_page_size_over_100(db_session):
    client = get_client(db_session)

    response = client.get(
        "/api/interviews?page_size=101"
    )

    assert response.status_code == 422


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
def clear_dependency_overrides(monkeypatch):
    monkeypatch.setenv(
        "JWT_SECRET_KEY",
        TEST_SECRET_KEY,
    )

    yield

    app.dependency_overrides.clear()
