from datetime import UTC, datetime
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from app.cli import follow_up_menu


def make_follow_up(
    follow_up_id=1,
    application_id=1,
    follow_up_at=None,
    note="Email recruiter",
    completed=False,
):
    return SimpleNamespace(
        id=follow_up_id,
        application_id=application_id,
        follow_up_at=(
            follow_up_at or datetime(2026, 8, 30, 10, 0, tzinfo=UTC)
        ),
        note=note,
        completed=completed,
    )


def test_add_follow_up():
    follow_up = make_follow_up()

    session = MagicMock()
    service = MagicMock()
    service.create_follow_up.return_value = follow_up

    with (
        patch.object(
            follow_up_menu,
            "SessionLocal",
            return_value=session,
        ),
        patch.object(
            follow_up_menu,
            "FollowUpService",
            return_value=service,
        ),
        patch(
            "builtins.input",
            side_effect=[
                "1",
                "2026-08-30 10:00",
                "Email recruiter",
            ],
        ),
    ):
        follow_up_menu.add_follow_up()

    service.create_follow_up.assert_called_once()

    created_follow_up = service.create_follow_up.call_args.args[0]

    assert created_follow_up.application_id == 1
    assert created_follow_up.follow_up_at == datetime(
        2026,
        8,
        30,
        10,
        0,
        tzinfo=UTC,
    )
    assert created_follow_up.note == "Email recruiter"


def test_add_follow_up_rejects_invalid_application_id(
    capsys,
):
    with patch(
        "builtins.input",
        return_value="abc",
    ):
        follow_up_menu.add_follow_up()

    output = capsys.readouterr().out

    assert "Application ID must be a number." in output


def test_add_follow_up_rejects_invalid_date(
    capsys,
):
    with patch(
        "builtins.input",
        side_effect=[
            "1",
            "invalid-date",
        ],
    ):
        follow_up_menu.add_follow_up()

    output = capsys.readouterr().out

    assert "Invalid date format." in output


def test_add_follow_up_rejects_invalid_follow_up_model(
    capsys,
):
    with patch(
        "builtins.input",
        side_effect=[
            "0",
            "2026-08-30 10:00",
            "Email recruiter",
        ],
    ):
        follow_up_menu.add_follow_up()

    output = capsys.readouterr().out

    assert "Error:" in output


def test_list_follow_ups(capsys):
    follow_ups = [
        make_follow_up(
            follow_up_id=1,
            application_id=1,
            note="Email recruiter",
        ),
        make_follow_up(
            follow_up_id=2,
            application_id=2,
            note="Submit documents",
            completed=True,
        ),
    ]

    session = MagicMock()
    service = MagicMock()
    service.get_follow_ups.return_value = follow_ups

    with (
        patch.object(
            follow_up_menu,
            "SessionLocal",
            return_value=session,
        ),
        patch.object(
            follow_up_menu,
            "FollowUpService",
            return_value=service,
        ),
    ):
        follow_up_menu.list_follow_ups()

    output = capsys.readouterr().out

    assert "Email recruiter" in output
    assert "Submit documents" in output
    assert "Pending" in output
    assert "Completed" in output


def test_list_follow_ups_when_empty(capsys):
    session = MagicMock()
    service = MagicMock()
    service.get_follow_ups.return_value = []

    with (
        patch.object(
            follow_up_menu,
            "SessionLocal",
            return_value=session,
        ),
        patch.object(
            follow_up_menu,
            "FollowUpService",
            return_value=service,
        ),
    ):
        follow_up_menu.list_follow_ups()

    output = capsys.readouterr().out

    assert "No follow-ups found." in output


def test_view_follow_up_with_invalid_id(capsys):
    with patch(
        "builtins.input",
        return_value="abc",
    ):
        follow_up_menu.view_follow_up()

    output = capsys.readouterr().out

    assert "Follow-Up ID must be a number." in output


def test_view_follow_up_not_found(capsys):
    session = MagicMock()
    service = MagicMock()
    service.get_follow_up.return_value = None

    with (
        patch.object(
            follow_up_menu,
            "SessionLocal",
            return_value=session,
        ),
        patch.object(
            follow_up_menu,
            "FollowUpService",
            return_value=service,
        ),
        patch(
            "builtins.input",
            return_value="999",
        ),
    ):
        follow_up_menu.view_follow_up()

    output = capsys.readouterr().out

    assert "Follow-up not found." in output


def test_view_follow_up(capsys):
    follow_up = make_follow_up(
        note="Email recruiter",
        completed=False,
    )

    session = MagicMock()
    service = MagicMock()
    service.get_follow_up.return_value = follow_up

    with (
        patch.object(
            follow_up_menu,
            "SessionLocal",
            return_value=session,
        ),
        patch.object(
            follow_up_menu,
            "FollowUpService",
            return_value=service,
        ),
        patch(
            "builtins.input",
            return_value="1",
        ),
    ):
        follow_up_menu.view_follow_up()

    output = capsys.readouterr().out

    assert "Follow-Up Details" in output
    assert "Application ID: 1" in output
    assert "Email recruiter" in output
    assert "Pending" in output


def test_complete_follow_up():
    follow_up = make_follow_up(
        completed=True,
    )

    session = MagicMock()
    service = MagicMock()
    service.complete_follow_up.return_value = follow_up

    with (
        patch.object(
            follow_up_menu,
            "SessionLocal",
            return_value=session,
        ),
        patch.object(
            follow_up_menu,
            "FollowUpService",
            return_value=service,
        ),
        patch(
            "builtins.input",
            return_value="1",
        ),
    ):
        follow_up_menu.complete_follow_up()

    service.complete_follow_up.assert_called_once_with(1)


def test_complete_follow_up_not_found(capsys):
    session = MagicMock()
    service = MagicMock()
    service.complete_follow_up.return_value = None

    with (
        patch.object(
            follow_up_menu,
            "SessionLocal",
            return_value=session,
        ),
        patch.object(
            follow_up_menu,
            "FollowUpService",
            return_value=service,
        ),
        patch(
            "builtins.input",
            return_value="999",
        ),
    ):
        follow_up_menu.complete_follow_up()

    output = capsys.readouterr().out

    assert "Follow-up not found." in output


def test_complete_follow_up_invalid_id(capsys):
    with patch(
        "builtins.input",
        return_value="abc",
    ):
        follow_up_menu.complete_follow_up()

    output = capsys.readouterr().out

    assert "Follow-Up ID must be a number." in output


def test_reopen_follow_up():
    follow_up = make_follow_up(
        completed=False,
    )

    session = MagicMock()
    service = MagicMock()
    service.reopen_follow_up.return_value = follow_up

    with (
        patch.object(
            follow_up_menu,
            "SessionLocal",
            return_value=session,
        ),
        patch.object(
            follow_up_menu,
            "FollowUpService",
            return_value=service,
        ),
        patch(
            "builtins.input",
            return_value="1",
        ),
    ):
        follow_up_menu.reopen_follow_up()

    service.reopen_follow_up.assert_called_once_with(1)


def test_reopen_follow_up_not_found(capsys):
    session = MagicMock()
    service = MagicMock()
    service.reopen_follow_up.return_value = None

    with (
        patch.object(
            follow_up_menu,
            "SessionLocal",
            return_value=session,
        ),
        patch.object(
            follow_up_menu,
            "FollowUpService",
            return_value=service,
        ),
        patch(
            "builtins.input",
            return_value="999",
        ),
    ):
        follow_up_menu.reopen_follow_up()

    output = capsys.readouterr().out

    assert "Follow-up not found." in output


def test_reopen_follow_up_invalid_id(capsys):
    with patch(
        "builtins.input",
        return_value="abc",
    ):
        follow_up_menu.reopen_follow_up()

    output = capsys.readouterr().out

    assert "Follow-Up ID must be a number." in output


def test_delete_follow_up():
    session = MagicMock()
    service = MagicMock()
    service.delete_follow_up.return_value = True

    with (
        patch.object(
            follow_up_menu,
            "SessionLocal",
            return_value=session,
        ),
        patch.object(
            follow_up_menu,
            "FollowUpService",
            return_value=service,
        ),
        patch(
            "builtins.input",
            return_value="1",
        ),
    ):
        follow_up_menu.delete_follow_up()

    service.delete_follow_up.assert_called_once_with(1)


def test_delete_follow_up_not_found(capsys):
    session = MagicMock()
    service = MagicMock()
    service.delete_follow_up.return_value = False

    with (
        patch.object(
            follow_up_menu,
            "SessionLocal",
            return_value=session,
        ),
        patch.object(
            follow_up_menu,
            "FollowUpService",
            return_value=service,
        ),
        patch(
            "builtins.input",
            return_value="999",
        ),
    ):
        follow_up_menu.delete_follow_up()

    output = capsys.readouterr().out

    assert "Follow-up not found." in output


def test_delete_follow_up_invalid_id(capsys):
    with patch(
        "builtins.input",
        return_value="abc",
    ):
        follow_up_menu.delete_follow_up()

    output = capsys.readouterr().out

    assert "Follow-Up ID must be a number." in output


def test_upcoming_follow_ups(capsys):
    follow_ups = [
        make_follow_up(
            follow_up_id=1,
            note="Email recruiter",
        ),
    ]

    session = MagicMock()
    service = MagicMock()
    service.get_upcoming_follow_ups.return_value = follow_ups

    with (
        patch.object(
            follow_up_menu,
            "SessionLocal",
            return_value=session,
        ),
        patch.object(
            follow_up_menu,
            "FollowUpService",
            return_value=service,
        ),
    ):
        follow_up_menu.upcoming_follow_ups()

    output = capsys.readouterr().out

    assert "Upcoming Follow-Ups" in output
    assert "Email recruiter" in output


def test_upcoming_follow_ups_when_empty(capsys):
    session = MagicMock()
    service = MagicMock()
    service.get_upcoming_follow_ups.return_value = []

    with (
        patch.object(
            follow_up_menu,
            "SessionLocal",
            return_value=session,
        ),
        patch.object(
            follow_up_menu,
            "FollowUpService",
            return_value=service,
        ),
    ):
        follow_up_menu.upcoming_follow_ups()

    output = capsys.readouterr().out

    assert "No upcoming follow-ups." in output


def test_pending_follow_ups(capsys):
    follow_ups = [
        make_follow_up(
            note="Email recruiter",
            completed=False,
        ),
    ]

    session = MagicMock()
    service = MagicMock()
    service.get_pending_follow_ups.return_value = follow_ups

    with (
        patch.object(
            follow_up_menu,
            "SessionLocal",
            return_value=session,
        ),
        patch.object(
            follow_up_menu,
            "FollowUpService",
            return_value=service,
        ),
    ):
        follow_up_menu.list_pending_follow_ups()

    output = capsys.readouterr().out

    assert "Pending Follow-Ups" in output
    assert "Email recruiter" in output


def test_pending_follow_ups_when_empty(capsys):
    session = MagicMock()
    service = MagicMock()
    service.get_pending_follow_ups.return_value = []

    with (
        patch.object(
            follow_up_menu,
            "SessionLocal",
            return_value=session,
        ),
        patch.object(
            follow_up_menu,
            "FollowUpService",
            return_value=service,
        ),
    ):
        follow_up_menu.list_pending_follow_ups()

    output = capsys.readouterr().out

    assert "No pending follow-ups." in output


def test_completed_follow_ups(capsys):
    follow_ups = [
        make_follow_up(
            note="Interview completed",
            completed=True,
        ),
    ]

    session = MagicMock()
    service = MagicMock()
    service.get_completed_follow_ups.return_value = follow_ups

    with (
        patch.object(
            follow_up_menu,
            "SessionLocal",
            return_value=session,
        ),
        patch.object(
            follow_up_menu,
            "FollowUpService",
            return_value=service,
        ),
    ):
        follow_up_menu.list_completed_follow_ups()

    output = capsys.readouterr().out

    assert "Completed Follow-Ups" in output
    assert "Interview completed" in output


def test_completed_follow_ups_when_empty(capsys):
    session = MagicMock()
    service = MagicMock()
    service.get_completed_follow_ups.return_value = []

    with (
        patch.object(
            follow_up_menu,
            "SessionLocal",
            return_value=session,
        ),
        patch.object(
            follow_up_menu,
            "FollowUpService",
            return_value=service,
        ),
    ):
        follow_up_menu.list_completed_follow_ups()

    output = capsys.readouterr().out

    assert "No completed follow-ups." in output
