import pytest
from fastapi.testclient import TestClient

from app.api.dependencies import get_db
from app.api.main import app
from app.database.models.company import CompanyDB
from app.database.models.user import UserDB
from app.security.jwt import create_access_token
TEST_SECRET_KEY = (
    "test-secret-key-for-companies-hs256-with-32-bytes-minimum"
)

def get_client(db_session):
    app.dependency_overrides[get_db] = lambda: db_session

    user = UserDB(
        email="company-user@example.com",
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

def test_create_company_requires_authentication(
    db_session,
):
    client = get_unauthenticated_client(db_session)

    response = client.post(
        "/api/companies",
        json={
            "name": "Microsoft",
            "website": "https://www.microsoft.com/",
            "industry": "Technology",
            "location": "Redmond, WA",
            "notes": "Software engineering opportunities",
        },
    )

    assert response.status_code == 401
    assert response.headers["WWW-Authenticate"] == "Bearer"
    assert response.json() == {
        "detail": "Could not validate credentials."
    }

def test_user_cannot_access_another_users_company(
    db_session,
):
    owner_client = get_client(db_session)

    create_response = owner_client.post(
        "/api/companies",
        json={
            "name": "Private Company",
            "website": "https://example.com",
        },
    )

    assert create_response.status_code == 201

    company_id = create_response.json()["id"]

    other_user = UserDB(
        email="other-user@example.com",
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
        f"/api/companies/{company_id}"
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Company not found."
    }

def test_user_cannot_list_another_users_company(
    db_session,
):
    owner_client = get_client(db_session)

    create_response = owner_client.post(
        "/api/companies",
        json={
            "name": "Private List Company",
            "website": "https://example.com",
        },
    )

    assert create_response.status_code == 201

    other_user = UserDB(
        email="other-company-list-user@example.com",
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
        "/api/companies"
    )

    assert response.status_code == 200
    assert response.json() == []

def test_user_cannot_update_another_users_company(
    db_session,
):
    owner_client = get_client(db_session)

    create_response = owner_client.post(
        "/api/companies",
        json={
            "name": "Private Update Company",
            "website": "https://example.com",
        },
    )

    assert create_response.status_code == 201

    company_id = create_response.json()["id"]

    other_user = UserDB(
        email="other-company-update-user@example.com",
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

    response = other_client.put(
        f"/api/companies/{company_id}",
        json={
            "name": "Hacked Company Name",
            "website": "https://attacker.example.com",
        },
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Company not found."
    }

    saved_company = db_session.get(
        CompanyDB,
        company_id,
    )

    assert saved_company is not None
    assert saved_company.name == "Private Update Company"
    assert saved_company.website == "https://example.com"

def test_user_cannot_delete_another_users_company(
    db_session,
):
    owner_client = get_client(db_session)

    create_response = owner_client.post(
        "/api/companies",
        json={
            "name": "Private Delete Company",
            "website": "https://example.com",
        },
    )

    assert create_response.status_code == 201

    company_id = create_response.json()["id"]

    other_user = UserDB(
        email="other-company-delete-user@example.com",
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

    response = other_client.delete(
        f"/api/companies/{company_id}"
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Company not found."
    }

    saved_company = db_session.get(
        CompanyDB,
        company_id,
    )

    assert saved_company is not None
    assert saved_company.name == "Private Delete Company"

def test_create_company(db_session):
    client = get_client(db_session)

    response = client.post(
        "/api/companies",
        json={
            "name": "Microsoft",
            "website": "https://www.microsoft.com/",
            "industry": "Technology",
            "location": "Redmond, WA",
            "notes": "Software engineering opportunities",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["id"] == 1
    assert data["name"] == "Microsoft"
    assert data["industry"] == "Technology"


def test_get_companies(db_session):
    company = CompanyDB(
        name="Microsoft",
        website="https://www.microsoft.com/",
        industry="Technology",
        location="Redmond, WA",
        notes="Software engineering opportunities",
    )

    db_session.add(company)
    db_session.commit()

    client = get_client(db_session)

    response = client.get("/api/companies")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["name"] == "Microsoft"


def test_get_companies_pagination(db_session):
    companies = [
        CompanyDB(name=f"Company {index}")
        for index in range(1, 26)
    ]

    db_session.add_all(companies)
    db_session.commit()

    client = get_client(db_session)

    response = client.get(
        "/api/companies?page=2&page_size=10"
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 10
    assert data[0]["name"] == "Company 11"
    assert data[-1]["name"] == "Company 20"


def test_get_companies_pagination_last_page(db_session):
    companies = [
        CompanyDB(name=f"Company {index}")
        for index in range(1, 26)
    ]

    db_session.add_all(companies)
    db_session.commit()

    client = get_client(db_session)

    response = client.get(
        "/api/companies?page=3&page_size=10"
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 5
    assert data[0]["name"] == "Company 21"
    assert data[-1]["name"] == "Company 25"


def test_get_companies_rejects_invalid_page(db_session):
    client = get_client(db_session)

    response = client.get(
        "/api/companies?page=0"
    )

    assert response.status_code == 422


def test_get_companies_rejects_invalid_page_size(db_session):
    client = get_client(db_session)

    response = client.get(
        "/api/companies?page_size=0"
    )

    assert response.status_code == 422


def test_get_companies_rejects_page_size_over_100(db_session):
    client = get_client(db_session)

    response = client.get(
        "/api/companies?page_size=101"
    )

    assert response.status_code == 422


def test_get_company(db_session):
    company = CompanyDB(
        name="Microsoft",
        website="https://www.microsoft.com/",
        industry="Technology",
        location="Redmond, WA",
    )

    db_session.add(company)
    db_session.commit()

    client = get_client(db_session)

    response = client.get("/api/companies/1")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == 1
    assert data["name"] == "Microsoft"


def test_get_company_not_found(db_session):
    client = get_client(db_session)

    response = client.get("/api/companies/999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Company not found."
    }


def test_update_company(db_session):
    company = CompanyDB(
        name="Microsoft",
        website="https://www.microsoft.com/",
        industry="Technology",
        location="Redmond, WA",
        notes="Original notes",
    )

    db_session.add(company)
    db_session.commit()

    client = get_client(db_session)

    response = client.put(
        "/api/companies/1",
        json={
            "name": "Microsoft Corporation",
            "website": "https://www.microsoft.com/",
            "industry": "Technology",
            "location": "Redmond, Washington",
            "notes": "Updated through API tests",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == 1
    assert data["name"] == "Microsoft Corporation"
    assert data["location"] == "Redmond, Washington"
    assert data["notes"] == "Updated through API tests"


def test_update_company_not_found(db_session):
    client = get_client(db_session)

    response = client.put(
        "/api/companies/999",
        json={
            "name": "Unknown Company",
        },
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Company not found."
    }


def test_delete_company(db_session):
    company = CompanyDB(
        name="Microsoft",
    )

    db_session.add(company)
    db_session.commit()

    client = get_client(db_session)

    response = client.delete("/api/companies/1")

    assert response.status_code == 204
    assert db_session.get(CompanyDB, 1) is None

def test_delete_company_not_found(db_session):
    client = get_client(db_session)

    response = client.delete("/api/companies/999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Company not found."
    }


@pytest.fixture(autouse=True)
def clear_dependency_overrides(monkeypatch):
    monkeypatch.setenv(
        "JWT_SECRET_KEY",
        TEST_SECRET_KEY,
    )

    yield

    app.dependency_overrides.clear()