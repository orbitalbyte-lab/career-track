from datetime import datetime, timezone

import pytest
from fastapi.testclient import TestClient

from app.api.dependencies import get_db
from app.api.main import app
from app.database.models.application import ApplicationDB
from app.database.models.company import CompanyDB
from app.database.models.follow_up import FollowUpDB


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


def test_create_follow_up(db_session):
    application = create_application(db_session)

    client = get_client(db_session)

    response = client.post(
        "/api/follow-ups",
        json={
            "application_id": application.id,
            "follow_up_at": "2026-09-20T10:00:00Z",
            "note": "Follow up with recruiter",
            "completed": False,
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["id"] == 1
    assert data["application_id"] == application.id
    assert data["note"] == "Follow up with recruiter"
    assert data["completed"] is False


def test_get_follow_ups(db_session):
    application = create_application(db_session)

    follow_up = FollowUpDB(
        application_id=application.id,
        follow_up_at=datetime(
            2026,
            9,
            20,
            10,
            0,
            tzinfo=timezone.utc,
        ),
        note="Follow up with recruiter",
        completed=False,
    )

    db_session.add(follow_up)
    db_session.commit()

    client = get_client(db_session)

    response = client.get("/api/follow-ups")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["id"] == 1
    assert data[0]["application_id"] == application.id
    assert data[0]["note"] == "Follow up with recruiter"
    assert data[0]["completed"] is False


def test_get_follow_up(db_session):
    application = create_application(db_session)

    follow_up = FollowUpDB(
        application_id=application.id,
        follow_up_at=datetime(
            2026,
            9,
            20,
            10,
            0,
            tzinfo=timezone.utc,
        ),
        note="Follow up with recruiter",
        completed=False,
    )

    db_session.add(follow_up)
    db_session.commit()

    client = get_client(db_session)

    response = client.get("/api/follow-ups/1")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == 1
    assert data["application_id"] == application.id
    assert data["note"] == "Follow up with recruiter"
    assert data["completed"] is False


def test_get_follow_up_not_found(db_session):
    client = get_client(db_session)

    response = client.get("/api/follow-ups/999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Follow-up not found."
    }


def test_complete_follow_up(db_session):
    application = create_application(db_session)

    follow_up = FollowUpDB(
        application_id=application.id,
        follow_up_at=datetime(
            2026,
            9,
            20,
            10,
            0,
            tzinfo=timezone.utc,
        ),
        note="Follow up with recruiter",
        completed=False,
    )

    db_session.add(follow_up)
    db_session.commit()

    client = get_client(db_session)

    response = client.put(
        "/api/follow-ups/1",
        json={
            "completed": True,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == 1
    assert data["completed"] is True


def test_reopen_follow_up(db_session):
    application = create_application(db_session)

    follow_up = FollowUpDB(
        application_id=application.id,
        follow_up_at=datetime(
            2026,
            9,
            20,
            10,
            0,
            tzinfo=timezone.utc,
        ),
        note="Follow up with recruiter",
        completed=True,
    )

    db_session.add(follow_up)
    db_session.commit()

    client = get_client(db_session)

    response = client.put(
        "/api/follow-ups/1",
        json={
            "completed": False,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == 1
    assert data["completed"] is False


def test_update_follow_up_not_found(db_session):
    client = get_client(db_session)

    response = client.put(
        "/api/follow-ups/999",
        json={
            "completed": True,
        },
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Follow-up not found."
    }


def test_delete_follow_up(db_session):
    application = create_application(db_session)

    follow_up = FollowUpDB(
        application_id=application.id,
        follow_up_at=datetime(
            2026,
            9,
            20,
            10,
            0,
            tzinfo=timezone.utc,
        ),
        note="Follow up with recruiter",
        completed=False,
    )

    db_session.add(follow_up)
    db_session.commit()

    client = get_client(db_session)

    response = client.delete("/api/follow-ups/1")

    assert response.status_code == 204
    assert db_session.get(FollowUpDB, 1) is None


def test_delete_follow_up_not_found(db_session):
    client = get_client(db_session)

    response = client.delete("/api/follow-ups/999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Follow-up not found."
    }


@pytest.fixture(autouse=True)
def clear_dependency_overrides():
    yield
    app.dependency_overrides.clear()
