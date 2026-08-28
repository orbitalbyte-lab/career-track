from datetime import datetime

from app.models.follow_up import FollowUp
from app.repositories.follow_up_repository import (
    FollowUpRepository,
)


def test_create_follow_up(db_session):
    repository = FollowUpRepository(
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

    result = repository.create(
        follow_up
    )

    assert result.id == 1
    assert result.application_id == 1
    assert result.note == "Email recruiter"
    assert result.completed is False


def test_get_all_follow_ups(db_session):
    repository = FollowUpRepository(
        db_session
    )

    repository.create(
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

    results = repository.get_all()

    assert len(results) == 1


def test_update_follow_up_completion(db_session):
    repository = FollowUpRepository(
        db_session
    )

    created = repository.create(
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

    result = repository.update(
        created.id,
        True,
    )

    assert result.completed is True


def test_delete_follow_up(db_session):
    repository = FollowUpRepository(
        db_session
    )

    created = repository.create(
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

    result = repository.delete(
        created.id
    )

    assert result is True

    assert (
        repository.get_by_id(
            created.id
        )
        is None
    )


def test_get_pending_follow_ups(db_session):
    repository = FollowUpRepository(
        db_session
    )

    repository.create(
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

    repository.create(
        FollowUp(
            application_id=1,
            follow_up_at=datetime(
                2026,
                8,
                1,
                10,
                0,
            ),
            note="Completed follow-up",
            completed=True,
        )
    )

    results = repository.get_pending()

    assert len(results) == 1
    assert (
        results[0].note
        == "Pending follow-up"
    )


def test_get_completed_follow_ups(db_session):
    repository = FollowUpRepository(
        db_session
    )

    repository.create(
        FollowUp(
            application_id=1,
            follow_up_at=datetime(
                2026,
                8,
                30,
                10,
                0,
            ),
            note="Completed follow-up",
            completed=True,
        )
    )

    results = repository.get_completed()

    assert len(results) == 1
    assert (
        results[0].completed is True
    )