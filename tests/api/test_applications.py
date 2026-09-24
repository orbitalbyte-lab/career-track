from datetime import date

import pytest
from fastapi.testclient import TestClient

from app.api.dependencies import get_db
from app.api.main import app
from app.database.models.application import ApplicationDB
from app.database.models.company import CompanyDB
from app.database.models.user import UserDB
from app.security.jwt import create_access_token
TEST_SECRET_KEY = (
    "test-secret-key-for-application-auth-hs256-with-32-bytes-minimum"
)

def get_client(db_session):
    app.dependency_overrides[get_db] = lambda: db_session

    user = UserDB(
        email="application-user@example.com",
        password_hash="test-hash",
        is_active=True,
    )

    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    unowned_companies = (
        db_session.query(CompanyDB)
        .filter(CompanyDB.user_id.is_(None))
        .all()
    )

    for company in unowned_companies:
        company.user_id = user.id

    db_session.commit()

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


def get_authenticated_client(
    db_session,
    monkeypatch,
):
    monkeypatch.setenv(
        "JWT_SECRET_KEY",
        TEST_SECRET_KEY,
    )

    user = UserDB(
        email="application-user@example.com",
        password_hash="test-hash",
        is_active=True,
    )

    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    token = create_access_token(str(user.id))

    client = get_client(db_session)

    client.headers.update(
        {
            "Authorization": f"Bearer {token}",
        }
    )

    return client

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

def test_create_application_requires_authentication(
    db_session,
):
    client = get_unauthenticated_client(db_session)

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

    assert response.status_code == 401
    assert response.headers["WWW-Authenticate"] == "Bearer"
    assert response.json() == {
        "detail": "Could not validate credentials."
    }

def test_user_cannot_create_application_for_another_users_company(
    db_session,
):
    owner_client = get_client(db_session)

    company_response = owner_client.post(
        "/api/companies",
        json={
            "name": "Private Company",
            "website": "https://example.com",
        },
    )

    assert company_response.status_code == 201

    company_id = company_response.json()["id"]

    other_user = UserDB(
        email="other-application-user@example.com",
        password_hash="test-hash",
        is_active=True,
    )

    db_session.add(other_user)
    db_session.commit()
    db_session.refresh(other_user)

    other_token = create_access_token(
        str(other_user.id)
    )

    other_client = TestClient(app)

    other_client.headers.update(
        {
            "Authorization": f"Bearer {other_token}",
        }
    )

    response = other_client.post(
        "/api/applications",
        json={
            "company_id": company_id,
            "position": "Software Engineering Intern",
            "application_type": "Internship",
            "date_applied": "2026-09-05",
            "status": "Applied",
        },
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "Company not found",
    }

def test_user_cannot_access_another_users_application(
    db_session,
):
    owner_client = get_client(db_session)

    company_response = owner_client.post(
        "/api/companies",
        json={
            "name": "Private Application Company",
            "website": "https://example.com",
        },
    )

    assert company_response.status_code == 201

    company_id = company_response.json()["id"]

    application_response = owner_client.post(
        "/api/applications",
        json={
            "company_id": company_id,
            "position": "Private Software Engineering Intern",
            "application_type": "Internship",
            "date_applied": "2026-09-05",
            "status": "Applied",
        },
    )

    assert application_response.status_code == 201

    application_id = application_response.json()["id"]

    other_user = UserDB(
        email="another-application-user@example.com",
        password_hash="test-hash",
        is_active=True,
    )

    db_session.add(other_user)
    db_session.commit()
    db_session.refresh(other_user)

    other_token = create_access_token(
        str(other_user.id)
    )

    other_client = TestClient(app)

    other_client.headers.update(
        {
            "Authorization": f"Bearer {other_token}",
        }
    )

    response = other_client.get(
        f"/api/applications/{application_id}"
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Application not found.",
    }

def test_user_cannot_list_another_users_application(
    db_session,
):
    owner_client = get_client(db_session)

    company_response = owner_client.post(
        "/api/companies",
        json={
            "name": "Private Application List Company",
            "website": "https://example.com",
        },
    )

    assert company_response.status_code == 201

    application_response = owner_client.post(
        "/api/applications",
        json={
            "company_id": company_response.json()["id"],
            "position": "Private List Position",
            "application_type": "Internship",
            "date_applied": "2026-09-05",
            "status": "Applied",
        },
    )

    assert application_response.status_code == 201

    other_user = UserDB(
        email="other-application-list-user@example.com",
        password_hash="test-hash",
        is_active=True,
    )

    db_session.add(other_user)
    db_session.commit()
    db_session.refresh(other_user)

    token = create_access_token(str(other_user.id))

    other_client = TestClient(app)
    other_client.headers.update(
        {
            "Authorization": f"Bearer {token}",
        }
    )

    response = other_client.get("/api/applications")

    assert response.status_code == 200
    assert response.json() == []

def test_user_cannot_update_another_users_application(
    db_session,
):
    owner_client = get_client(db_session)

    company_response = owner_client.post(
        "/api/companies",
        json={
            "name": "Private Application Update Company",
            "website": "https://example.com",
        },
    )

    assert company_response.status_code == 201

    application_response = owner_client.post(
        "/api/applications",
        json={
            "company_id": company_response.json()["id"],
            "position": "Private Update Position",
            "application_type": "Internship",
            "date_applied": "2026-09-05",
            "status": "Applied",
        },
    )

    assert application_response.status_code == 201

    application_id = application_response.json()["id"]

    other_user = UserDB(
        email="other-application-update-user@example.com",
        password_hash="test-hash",
        is_active=True,
    )

    db_session.add(other_user)
    db_session.commit()
    db_session.refresh(other_user)

    token = create_access_token(str(other_user.id))

    other_client = TestClient(app)
    other_client.headers.update(
        {
            "Authorization": f"Bearer {token}",
        }
    )

    response = other_client.put(
        f"/api/applications/{application_id}",
        json={
            "position": "Hacked Position",
            "status": "Offer",
        },
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Application not found.",
    }

    saved_application = db_session.get(
        ApplicationDB,
        application_id,
    )

    assert saved_application is not None
    assert saved_application.position == "Private Update Position"
    assert saved_application.status == "Applied"

def test_user_cannot_delete_another_users_application(
    db_session,
):
    owner_client = get_client(db_session)

    company_response = owner_client.post(
        "/api/companies",
        json={
            "name": "Private Application Delete Company",
            "website": "https://example.com",
        },
    )

    assert company_response.status_code == 201

    application_response = owner_client.post(
        "/api/applications",
        json={
            "company_id": company_response.json()["id"],
            "position": "Private Delete Position",
            "application_type": "Internship",
            "date_applied": "2026-09-05",
            "status": "Applied",
        },
    )

    assert application_response.status_code == 201

    application_id = application_response.json()["id"]

    other_user = UserDB(
        email="other-application-delete-user@example.com",
        password_hash="test-hash",
        is_active=True,
    )

    db_session.add(other_user)
    db_session.commit()
    db_session.refresh(other_user)

    token = create_access_token(str(other_user.id))

    other_client = TestClient(app)
    other_client.headers.update(
        {
            "Authorization": f"Bearer {token}",
        }
    )

    response = other_client.delete(
        f"/api/applications/{application_id}"
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Application not found.",
    }

    assert db_session.get(
        ApplicationDB,
        application_id,
    ) is not None

def test_create_application(
    db_session,
    monkeypatch,
):
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
    monkeypatch,
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

def test_create_application_company_not_found(
    db_session,
    monkeypatch,
):
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

def test_get_applications_filters_by_status(db_session):
    company = create_company(db_session)

    applied_application = ApplicationDB(
        company_id=company.id,
        position="Software Engineering Intern",
        application_type="Internship",
        date_applied=date(2026, 9, 5),
        status="Applied",
        location="Redmond, WA",
        job_url="https://www.microsoft.com/",
    )

    wishlist_application = ApplicationDB(
        company_id=company.id,
        position="Backend Engineering Intern",
        application_type="Internship",
        date_applied=date(2026, 9, 4),
        status="Wishlist",
        location="Seattle, WA",
        job_url="https://www.google.com/",
    )

    db_session.add_all(
        [
            applied_application,
            wishlist_application,
        ]
    )
    db_session.commit()

    client = get_client(db_session)

    response = client.get(
        "/api/applications?status=Applied"
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["position"] == "Software Engineering Intern"
    assert data[0]["status"] == "Applied"

def test_get_applications_filters_by_application_type(db_session):
    company = create_company(db_session)

    internship_application = ApplicationDB(
        company_id=company.id,
        position="Software Engineering Intern",
        application_type="Internship",
        date_applied=date(2026, 9, 5),
        status="Applied",
        location="Redmond, WA",
        job_url="https://www.microsoft.com/",
    )

    scholarship_application = ApplicationDB(
        company_id=company.id,
        position="Scholarship Program",
        application_type="Scholarship",
        date_applied=date(2026, 9, 4),
        status="Wishlist",
        location="Seattle, WA",
        job_url="https://www.google.com/",
    )

    db_session.add_all(
        [
            internship_application,
            scholarship_application,
        ]
    )
    db_session.commit()

    client = get_client(db_session)

    response = client.get(
        "/api/applications?application_type=Internship"
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["position"] == "Software Engineering Intern"
    assert data[0]["application_type"] == "Internship"

def test_get_applications_filters_by_company(db_session):
    microsoft = create_company(db_session)
    google = create_company(db_session)

    microsoft.name = "Microsoft"
    google.name = "Google"

    db_session.commit()

    microsoft_application = ApplicationDB(
        company_id=microsoft.id,
        position="Software Engineering Intern",
        application_type="Internship",
        date_applied=date(2026, 9, 5),
        status="Applied",
        location="Redmond, WA",
        job_url="https://www.microsoft.com/",
    )

    google_application = ApplicationDB(
        company_id=google.id,
        position="Backend Engineering Intern",
        application_type="Internship",
        date_applied=date(2026, 9, 4),
        status="Applied",
        location="Mountain View, CA",
        job_url="https://www.google.com/",
    )

    db_session.add_all(
        [
            microsoft_application,
            google_application,
        ]
    )
    db_session.commit()

    client = get_client(db_session)

    response = client.get(
        f"/api/applications?company_id={microsoft.id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["company_id"] == microsoft.id
    assert data[0]["position"] == "Software Engineering Intern"

def test_get_applications_filters_by_date_applied(db_session):
    company = create_company(db_session)

    matching_application = ApplicationDB(
        company_id=company.id,
        position="Software Engineering Intern",
        application_type="Internship",
        date_applied=date(2026, 9, 5),
        status="Applied",
        location="Redmond, WA",
        job_url="https://www.microsoft.com/",
    )

    other_application = ApplicationDB(
        company_id=company.id,
        position="Backend Engineering Intern",
        application_type="Internship",
        date_applied=date(2026, 9, 4),
        status="Applied",
        location="Seattle, WA",
        job_url="https://www.google.com/",
    )

    db_session.add_all(
        [
            matching_application,
            other_application,
        ]
    )
    db_session.commit()

    client = get_client(db_session)

    response = client.get(
        "/api/applications?date_applied=2026-09-05"
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["position"] == "Software Engineering Intern"
    assert data[0]["date_applied"] == "2026-09-05"

def test_get_applications_combined_filters_with_pagination(
    db_session,
):
    company = create_company(db_session)

    applications = [
        ApplicationDB(
            company_id=company.id,
            position=f"Intern {index}",
            application_type="Internship",
            date_applied=date(2026, 9, 10 - index),
            status="Applied",
            location="Redmond, WA",
            job_url="https://www.microsoft.com/",
        )
        for index in range(1, 6)
    ]

    wishlist_application = ApplicationDB(
        company_id=company.id,
        position="Wishlist Application",
        application_type="Internship",
        date_applied=date(2026, 9, 5),
        status="Wishlist",
        location="Seattle, WA",
        job_url="https://www.google.com/",
    )

    db_session.add_all(
        applications + [wishlist_application]
    )
    db_session.commit()

    client = get_client(db_session)

    response = client.get(
        "/api/applications"
        "?status=Applied"
        "&application_type=Internship"
        "&page=2"
        "&page_size=2"
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2
    assert data[0]["position"] == "Intern 3"
    assert data[1]["position"] == "Intern 4"

    for application in data:
        assert application["status"] == "Applied"
        assert application["application_type"] == "Internship"

def test_get_applications_returns_empty_for_no_filter_matches(
    db_session,
):
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

    response = client.get(
        "/api/applications?status=Offer"
    )

    assert response.status_code == 200
    assert response.json() == []

def test_get_applications_rejects_invalid_status_filter(
    db_session,
):
    client = get_client(db_session)

    response = client.get(
        "/api/applications?status=InvalidStatus"
    )

    assert response.status_code == 422


def test_get_applications_rejects_invalid_application_type_filter(
    db_session,
):
    client = get_client(db_session)

    response = client.get(
        "/api/applications?application_type=InvalidType"
    )

    assert response.status_code == 422

def test_get_applications_rejects_invalid_company_id(
    db_session,
):
    client = get_client(db_session)

    response = client.get(
        "/api/applications?company_id=0"
    )

    assert response.status_code == 422


def test_get_applications_rejects_invalid_date_applied(
    db_session,
):
    client = get_client(db_session)

    response = client.get(
        "/api/applications?date_applied=not-a-date"
    )

    assert response.status_code == 422

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

def test_update_application_rejects_deadline_before_application_date(
    db_session,
):
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

    response = client.put(
        "/api/applications/1",
        json={
            "date_applied": "2026-09-10",
            "deadline": "2026-09-05",
        },
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "Deadline cannot be before the application date"
    }

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
def clear_dependency_overrides(monkeypatch):
    monkeypatch.setenv(
        "JWT_SECRET_KEY",
        TEST_SECRET_KEY,
    )

    yield

    app.dependency_overrides.clear()