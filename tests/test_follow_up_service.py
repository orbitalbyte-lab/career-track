from datetime import datetime

from app.models.follow_up import FollowUp
from app.services.follow_up_service import (
    FollowUpService,
)


def test_create_follow_up(db_session):
    service = FollowUpService(
        db_session
    )

    follow_up = FollowUp(
        application_id=1,
        follow_up_at=datetime(
            2026,
            8,
            30,
            10,
            0,
        ),
        note="Email recruiter",
    )

    result = service.create_follow_up(
        follow_up
    )

    assert result.id == 1


def test_get_follow_ups(db_session):
    service = FollowUpService(
        db_session
    )

    service.create_follow_up(
        FollowUp(
            application_id=1,
            follow_up_at=datetime(
                2026,
                8,
                30,
                10,
                0,
            ),
            note="Email recruiter",
        )
    )

    results = service.get_follow_ups()

    assert len(results) == 1


def test_complete_follow_up(db_session):
    service = FollowUpService(
        db_session
    )

    created = service.create_follow_up(
        FollowUp(
            application_id=1,
            follow_up_at=datetime(
                2026,
                8,
                30,
                10,
                0,
            ),
            note="Email recruiter",
        )
    )

    result = service.complete_follow_up(
        created.id
    )

    assert result.completed is True


def test_reopen_follow_up(db_session):
    service = FollowUpService(
        db_session
    )

    created = service.create_follow_up(
        FollowUp(
            application_id=1,
            follow_up_at=datetime(
                2026,
                8,
                30,
                10,
                0,
            ),
            note="Email recruiter",
            completed=True,
        )
    )

    result = service.reopen_follow_up(
        created.id
    )

    assert result.completed is False


def test_delete_follow_up(db_session):
    service = FollowUpService(
        db_session
    )

    created = service.create_follow_up(
        FollowUp(
            application_id=1,
            follow_up_at=datetime(
                2026,
                8,
                30,
                10,
                0,
            ),
            note="Email recruiter",
        )
    )

    result = service.delete_follow_up(
        created.id
    )

    assert result is True


def test_follow_up_statistics(db_session):
    service = FollowUpService(
        db_session
    )

    service.create_follow_up(
        FollowUp(
            application_id=1,
            follow_up_at=datetime(
                2026,
                8,
                30,
                10,
                0,
            ),
            note="Pending follow-up",
        )
    )

    service.create_follow_up(
        FollowUp(
            application_id=2,
            follow_up_at=datetime(
                2026,
                9,
                1,
                10,
                0,
            ),
            note="Completed follow-up",
            completed=True,
        )
    )

    statistics = (
        service.get_follow_up_statistics()
    )

    assert statistics["total"] == 2
    assert statistics["pending"] == 1
    assert statistics["completed"] == 1