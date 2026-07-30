from datetime import date

import pytest

from app.models.application import (
    Application,
    ApplicationStatus,
    ApplicationType,
)


def test_application_defaults_to_wishlist():
    application = Application(
        company="Microsoft",
        position="Software Engineering Intern",
        application_type=ApplicationType.INTERNSHIP,
        date_applied=date(2026, 7, 30),
    )

    assert application.status == ApplicationStatus.WISHLIST


def test_application_can_have_status():
    application = Application(
        company="Google",
        position="Backend Engineering Intern",
        application_type=ApplicationType.INTERNSHIP,
        date_applied=date(2026, 7, 30),
        status=ApplicationStatus.APPLIED,
    )

    assert application.status == ApplicationStatus.APPLIED


def test_application_rejects_empty_company():
    with pytest.raises(ValueError, match="Company name cannot be empty"):
        Application(
            company="",
            position="Software Engineering Intern",
            application_type=ApplicationType.INTERNSHIP,
            date_applied=date(2026, 7, 30),
        )


def test_application_rejects_empty_position():
    with pytest.raises(ValueError, match="Position cannot be empty"):
        Application(
            company="Microsoft",
            position="",
            application_type=ApplicationType.INTERNSHIP,
            date_applied=date(2026, 7, 30),
        )


def test_application_rejects_invalid_deadline():
    with pytest.raises(
        ValueError,
        match="Deadline cannot be before the application date",
    ):
        Application(
            company="Microsoft",
            position="Software Engineering Intern",
            application_type=ApplicationType.INTERNSHIP,
            date_applied=date(2026, 7, 30),
            deadline=date(2026, 7, 29),
        )