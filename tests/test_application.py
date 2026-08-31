import pytest
from datetime import date

from app.models.application import (
    Application,
    ApplicationStatus,
    ApplicationType,
)
from app.models.company import Company


def test_application_defaults_to_wishlist():
    company = Company(name="Microsoft")

    application = Application(
        company=company,
        position="Software Engineering Intern",
        application_type=ApplicationType.INTERNSHIP,
        date_applied=date(2026, 7, 30),
    )

    assert application.status == ApplicationStatus.WISHLIST


def test_application_can_have_status():
    company = Company(name="Google")

    application = Application(
        company=company,
        position="Backend Engineering Intern",
        application_type=ApplicationType.INTERNSHIP,
        date_applied=date(2026, 7, 30),
        status=ApplicationStatus.APPLIED,
    )

    assert application.status == ApplicationStatus.APPLIED


def test_application_rejects_empty_company():
    with pytest.raises(ValueError, match="Company name cannot be empty"):
        company = Company(name="")

        Application(
            company=company,
            position="Software Engineering Intern",
            application_type=ApplicationType.INTERNSHIP,
            date_applied=date(2026, 7, 30),
        )


def test_application_rejects_empty_position():
    company = Company(name="Microsoft")

    with pytest.raises(ValueError, match="Position cannot be empty"):
        Application(
            company=company,
            position="",
            application_type=ApplicationType.INTERNSHIP,
            date_applied=date(2026, 7, 30),
        )


def test_application_rejects_invalid_deadline():
    company = Company(name="Microsoft")

    with pytest.raises(
        ValueError,
        match="Deadline cannot be before the application date",
    ):
        Application(
            company=company,
            position="Software Engineering Intern",
            application_type=ApplicationType.INTERNSHIP,
            date_applied=date(2026, 7, 30),
            deadline=date(2026, 7, 29),
        )


def test_application_accepts_valid_deadline():
    company = Company(name="Microsoft")

    application = Application(
        company=company,
        position="Software Engineering Intern",
        application_type=ApplicationType.INTERNSHIP,
        date_applied=date(2026, 7, 30),
        deadline=date(2026, 8, 15),
    )

    assert application.deadline == date(2026, 8, 15)


def test_application_accepts_valid_application_type():
    company = Company(name="Microsoft")

    application = Application(
        company=company,
        position="Software Engineering Intern",
        application_type=ApplicationType.INTERNSHIP,
        date_applied=date(2026, 7, 30),
    )

    assert application.application_type == ApplicationType.INTERNSHIP


def test_application_rejects_invalid_application_type():
    company = Company(name="Microsoft")

    with pytest.raises(ValueError, match="Invalid application type"):
        Application(
            company=company,
            position="Software Engineering Intern",
            application_type="Invalid",
            date_applied=date(2026, 7, 30),
        )
def test_application_rejects_invalid_application_type():
    company = Company(name="Google")

    with pytest.raises(
        ValueError,
        match="Invalid application type.",
    ):
        Application(
            company=company,
            position="Software Engineer",
            application_type="Full-time",
            date_applied=date(2026, 8, 20),
            status=ApplicationStatus.APPLIED,
        )


def test_application_rejects_invalid_status():
    company = Company(name="Microsoft")

    with pytest.raises(
        ValueError,
        match="Invalid application status",
    ):
        Application(
            company=company,
            position="Software Engineering Intern",
            application_type=ApplicationType.INTERNSHIP,
            date_applied=date(2026, 7, 30),
            status="Invalid",
        )