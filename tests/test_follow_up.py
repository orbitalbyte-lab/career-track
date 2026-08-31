from datetime import datetime

import pytest

from app.models.follow_up import FollowUp


def test_create_follow_up():
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

    assert follow_up.application_id == 1
    assert (
        follow_up.follow_up_at
        == datetime(
            2026,
            8,
            30,
            10,
            0,
        )
    )
    assert follow_up.note == "Email recruiter"
    assert follow_up.completed is False


def test_follow_up_can_be_completed():
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
        completed=True,
    )

    assert follow_up.completed is True


def test_follow_up_rejects_invalid_application_id():
    with pytest.raises(ValueError):
        FollowUp(
            application_id=0,
            follow_up_at=datetime(
                2026,
                8,
                30,
                10,
                0,
            ),
            note="Email recruiter",
        )


def test_follow_up_rejects_empty_note():
    with pytest.raises(ValueError):
        FollowUp(
            application_id=1,
            follow_up_at=datetime(
                2026,
                8,
                30,
                10,
                0,
            ),
            note="   ",
        )


def test_follow_up_rejects_invalid_completion_status():
    with pytest.raises(ValueError):
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
            completed="yes",
        )

def test_follow_up_rejects_invalid_follow_up_date():
    with pytest.raises(
        ValueError,
        match="Invalid follow-up date",
    ):
        FollowUp(
            application_id=1,
            follow_up_at="invalid date",
            note="Email recruiter",
        )        