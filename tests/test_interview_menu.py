from datetime import datetime
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from app.cli import interview_menu
from app.models.interview import (
    InterviewOutcome,
    InterviewStatus,
    InterviewType,
)


def make_interview(
    interview_id=1,
    application_id=1,
    scheduled_at=None,
    interview_type="Online",
    status="Scheduled",
    outcome="Pending",
    notes=None,
    application=None,
):
    return SimpleNamespace(
        id=interview_id,
        application_id=application_id,
        scheduled_at=(
            scheduled_at
            or datetime(2026, 9, 1, 10, 0)
        ),
        interview_type=interview_type,
        status=status,
        outcome=outcome,
        notes=notes,
        application=application,
    )


def test_add_interview():
    interview = make_interview()

    session = MagicMock()
    service = MagicMock()
    service.create_interview.return_value = interview

    with patch.object(
        interview_menu,
        "SessionLocal",
        return_value=session,
    ), patch.object(
        interview_menu,
        "InterviewService",
        return_value=service,
    ), patch(
        "builtins.input",
        side_effect=[
            "1",
            "2026-09-01 10:00",
            "Online",
            "Technical interview",
        ],
    ):
        interview_menu.add_interview()

    service.create_interview.assert_called_once()

    created = service.create_interview.call_args.args[0]

    assert created.application_id == 1
    assert created.scheduled_at == datetime(
        2026, 9, 1, 10, 0
    )
    assert created.interview_type == InterviewType.ONLINE
    assert created.outcome == InterviewOutcome.PENDING
    assert created.notes == "Technical interview"


def test_add_interview_retries_invalid_application_id():
    interview = make_interview()

    session = MagicMock()
    service = MagicMock()
    service.create_interview.return_value = interview

    with patch.object(
        interview_menu,
        "SessionLocal",
        return_value=session,
    ), patch.object(
        interview_menu,
        "InterviewService",
        return_value=service,
    ), patch(
        "builtins.input",
        side_effect=[
            "abc",
            "1",
            "2026-09-01 10:00",
            "Online",
            "",
        ],
    ):
        interview_menu.add_interview()

    output = service.create_interview.call_args.args[0]

    assert output.application_id == 1


def test_add_interview_retries_invalid_date(capsys):
    interview = make_interview()

    session = MagicMock()
    service = MagicMock()
    service.create_interview.return_value = interview

    with patch.object(
        interview_menu,
        "SessionLocal",
        return_value=session,
    ), patch.object(
        interview_menu,
        "InterviewService",
        return_value=service,
    ), patch(
        "builtins.input",
        side_effect=[
            "1",
            "bad-date",
            "2026-09-01 10:00",
            "Online",
            "",
        ],
    ):
        interview_menu.add_interview()

    output = capsys.readouterr().out

    assert (
        "Please enter the date as YYYY-MM-DD HH:MM."
        in output
    )


def test_add_interview_retries_invalid_type(capsys):
    interview = make_interview()

    session = MagicMock()
    service = MagicMock()
    service.create_interview.return_value = interview

    with patch.object(
        interview_menu,
        "SessionLocal",
        return_value=session,
    ), patch.object(
        interview_menu,
        "InterviewService",
        return_value=service,
    ), patch(
        "builtins.input",
        side_effect=[
            "1",
            "2026-09-01 10:00",
            "Invalid",
            "Online",
            "",
        ],
    ):
        interview_menu.add_interview()

    output = capsys.readouterr().out

    assert (
        "Please choose Online, Phone, or On-site."
        in output
    )


def test_list_interviews(capsys):
    interviews = [
        make_interview(
            interview_id=1,
            application_id=1,
            interview_type="Online",
            status="Scheduled",
        ),
        make_interview(
            interview_id=2,
            application_id=2,
            interview_type="Phone",
            status="Completed",
        ),
    ]

    session = MagicMock()
    service = MagicMock()
    service.get_interviews.return_value = interviews

    with patch.object(
        interview_menu,
        "SessionLocal",
        return_value=session,
    ), patch.object(
        interview_menu,
        "InterviewService",
        return_value=service,
    ):
        interview_menu.list_interviews()

    output = capsys.readouterr().out

    assert "Interview ID: 1" in output
    assert "Interview ID: 2" in output
    assert "Online" in output
    assert "Phone" in output
    assert "Scheduled" in output
    assert "Completed" in output


def test_list_interviews_when_empty(capsys):
    session = MagicMock()
    service = MagicMock()
    service.get_interviews.return_value = []

    with patch.object(
        interview_menu,
        "SessionLocal",
        return_value=session,
    ), patch.object(
        interview_menu,
        "InterviewService",
        return_value=service,
    ):
        interview_menu.list_interviews()

    output = capsys.readouterr().out

    assert "No interviews found." in output


def test_view_interview_invalid_id(capsys):
    with patch(
        "builtins.input",
        return_value="abc",
    ):
        interview_menu.view_interview()

    output = capsys.readouterr().out

    assert "Interview ID must be a number." in output


def test_view_interview_not_found(capsys):
    session = MagicMock()
    service = MagicMock()
    service.get_interview.return_value = None

    with patch.object(
        interview_menu,
        "SessionLocal",
        return_value=session,
    ), patch.object(
        interview_menu,
        "InterviewService",
        return_value=service,
    ), patch(
        "builtins.input",
        return_value="999",
    ):
        interview_menu.view_interview()

    output = capsys.readouterr().out

    assert "Interview not found." in output


def test_view_interview(capsys):
    company = SimpleNamespace(
        name="Microsoft"
    )

    application = SimpleNamespace(
        position="Software Engineering Intern",
        company=company,
    )

    interview = make_interview(
        application=application,
        interview_type="Online",
        status="Scheduled",
        outcome="Pending",
        notes="Prepare coding questions",
    )

    session = MagicMock()
    service = MagicMock()
    service.get_interview.return_value = interview

    with patch.object(
        interview_menu,
        "SessionLocal",
        return_value=session,
    ), patch.object(
        interview_menu,
        "InterviewService",
        return_value=service,
    ), patch(
        "builtins.input",
        return_value="1",
    ):
        interview_menu.view_interview()

    output = capsys.readouterr().out

    assert "Interview ID: 1" in output
    assert "Application ID: 1" in output
    assert "Company: Microsoft" in output
    assert "Position: Software Engineering Intern" in output
    assert "Online" in output
    assert "Scheduled" in output
    assert "Pending" in output
    assert "Prepare coding questions" in output


def test_update_interview():
    interview = make_interview(
        status="Completed",
        outcome="Passed",
    )

    session = MagicMock()
    service = MagicMock()
    service.update_interview.return_value = interview

    with patch.object(
        interview_menu,
        "SessionLocal",
        return_value=session,
    ), patch.object(
        interview_menu,
        "InterviewService",
        return_value=service,
    ), patch(
        "builtins.input",
        side_effect=[
            "1",
            "Completed",
            "Passed",
        ],
    ):
        interview_menu.update_interview()

    service.update_interview.assert_called_once_with(
        1,
        "Completed",
        "Passed",
    )


def test_update_interview_invalid_id(capsys):
    with patch(
        "builtins.input",
        return_value="abc",
    ):
        interview_menu.update_interview()

    output = capsys.readouterr().out

    assert "Please enter a valid ID." in output


def test_update_interview_invalid_status(capsys):
    with patch(
        "builtins.input",
        side_effect=[
            "1",
            "Invalid",
        ],
    ):
        interview_menu.update_interview()

    output = capsys.readouterr().out

    assert "Invalid status." in output


def test_update_interview_invalid_outcome(capsys):
    with patch(
        "builtins.input",
        side_effect=[
            "1",
            "Completed",
            "Invalid",
        ],
    ):
        interview_menu.update_interview()

    output = capsys.readouterr().out

    assert "Invalid outcome." in output


def test_update_interview_not_found(capsys):
    session = MagicMock()
    service = MagicMock()
    service.update_interview.return_value = None

    with patch.object(
        interview_menu,
        "SessionLocal",
        return_value=session,
    ), patch.object(
        interview_menu,
        "InterviewService",
        return_value=service,
    ), patch(
        "builtins.input",
        side_effect=[
            "999",
            "Completed",
            "Passed",
        ],
    ):
        interview_menu.update_interview()

    output = capsys.readouterr().out

    assert "Interview not found." in output


def test_delete_interview():
    session = MagicMock()
    service = MagicMock()
    service.delete_interview.return_value = True

    with patch.object(
        interview_menu,
        "SessionLocal",
        return_value=session,
    ), patch.object(
        interview_menu,
        "InterviewService",
        return_value=service,
    ), patch(
        "builtins.input",
        return_value="1",
    ):
        interview_menu.delete_interview()

    service.delete_interview.assert_called_once_with(1)


def test_delete_interview_invalid_id(capsys):
    with patch(
        "builtins.input",
        return_value="abc",
    ):
        interview_menu.delete_interview()

    output = capsys.readouterr().out

    assert "Please enter a valid ID." in output


def test_delete_interview_not_found(capsys):
    session = MagicMock()
    service = MagicMock()
    service.delete_interview.return_value = False

    with patch.object(
        interview_menu,
        "SessionLocal",
        return_value=session,
    ), patch.object(
        interview_menu,
        "InterviewService",
        return_value=service,
    ), patch(
        "builtins.input",
        return_value="999",
    ):
        interview_menu.delete_interview()

    output = capsys.readouterr().out

    assert "Interview not found." in output


def test_search_interviews(capsys):
    interviews = [
        make_interview(
            interview_type="Online",
            status="Scheduled",
        )
    ]

    session = MagicMock()
    service = MagicMock()
    service.search_interviews.return_value = interviews

    with patch.object(
        interview_menu,
        "SessionLocal",
        return_value=session,
    ), patch.object(
        interview_menu,
        "InterviewService",
        return_value=service,
    ), patch(
        "builtins.input",
        return_value="Scheduled",
    ):
        interview_menu.search_interviews()

    service.search_interviews.assert_called_once_with(
        "Scheduled"
    )

    output = capsys.readouterr().out

    assert "Interview ID: 1" in output
    assert "Scheduled" in output


def test_search_interviews_when_empty(capsys):
    session = MagicMock()
    service = MagicMock()
    service.search_interviews.return_value = []

    with patch.object(
        interview_menu,
        "SessionLocal",
        return_value=session,
    ), patch.object(
        interview_menu,
        "InterviewService",
        return_value=service,
    ), patch(
        "builtins.input",
        return_value="Nothing",
    ):
        interview_menu.search_interviews()

    output = capsys.readouterr().out

    assert "No interviews found." in output


def test_filter_interviews(capsys):
    interviews = [
        make_interview(
            status="Scheduled"
        )
    ]

    session = MagicMock()
    service = MagicMock()
    service.get_interviews_by_status.return_value = interviews

    with patch.object(
        interview_menu,
        "SessionLocal",
        return_value=session,
    ), patch.object(
        interview_menu,
        "InterviewService",
        return_value=service,
    ), patch(
        "builtins.input",
        return_value="Scheduled",
    ):
        interview_menu.filter_interviews()

    service.get_interviews_by_status.assert_called_once_with(
        "Scheduled"
    )

    output = capsys.readouterr().out

    assert "Interview ID: 1" in output


def test_filter_interviews_when_empty(capsys):
    session = MagicMock()
    service = MagicMock()
    service.get_interviews_by_status.return_value = []

    with patch.object(
        interview_menu,
        "SessionLocal",
        return_value=session,
    ), patch.object(
        interview_menu,
        "InterviewService",
        return_value=service,
    ), patch(
        "builtins.input",
        return_value="Completed",
    ):
        interview_menu.filter_interviews()

    output = capsys.readouterr().out

    assert "No interviews found." in output


def test_sort_interviews_by_date(capsys):
    interviews = [
        make_interview(
            interview_id=2,
            scheduled_at=datetime(
                2026, 9, 5, 10, 0
            ),
        ),
        make_interview(
            interview_id=1,
            scheduled_at=datetime(
                2026, 9, 1, 10, 0
            ),
        ),
    ]

    session = MagicMock()
    service = MagicMock()
    service.get_sorted_interviews.return_value = interviews

    with patch.object(
        interview_menu,
        "SessionLocal",
        return_value=session,
    ), patch.object(
        interview_menu,
        "InterviewService",
        return_value=service,
    ), patch(
        "builtins.input",
        return_value="1",
    ):
        interview_menu.sort_interviews()

    service.get_sorted_interviews.assert_called_once_with(
        "date"
    )

    output = capsys.readouterr().out

    assert "Interviews (Newest First)" in output
    assert "[2]" in output


def test_sort_interviews_by_type(capsys):
    interviews = [
        make_interview(
            interview_id=1,
            interview_type="Online",
        ),
        make_interview(
            interview_id=2,
            interview_type="Phone",
        ),
    ]

    session = MagicMock()
    service = MagicMock()
    service.get_sorted_interviews.return_value = interviews

    with patch.object(
        interview_menu,
        "SessionLocal",
        return_value=session,
    ), patch.object(
        interview_menu,
        "InterviewService",
        return_value=service,
    ), patch(
        "builtins.input",
        return_value="2",
    ):
        interview_menu.sort_interviews()

    service.get_sorted_interviews.assert_called_once_with(
        "type"
    )

    output = capsys.readouterr().out

    assert "Interviews (Type A-Z)" in output
    assert "Online" in output
    assert "Phone" in output


def test_sort_interviews_invalid_option(capsys):
    with patch(
        "builtins.input",
        return_value="9",
    ):
        interview_menu.sort_interviews()

    output = capsys.readouterr().out

    assert "Invalid sorting option." in output


def test_sort_interviews_when_empty(capsys):
    session = MagicMock()
    service = MagicMock()
    service.get_sorted_interviews.return_value = []

    with patch.object(
        interview_menu,
        "SessionLocal",
        return_value=session,
    ), patch.object(
        interview_menu,
        "InterviewService",
        return_value=service,
    ), patch(
        "builtins.input",
        return_value="1",
    ):
        interview_menu.sort_interviews()

    output = capsys.readouterr().out

    assert "No interviews found." in output


def test_export_interviews():
    session = MagicMock()
    interview_service = MagicMock()
    exporter = MagicMock()

    exporter.export_interviews_to_csv.return_value = (
        "exports/interviews.csv"
    )

    with patch.object(
        interview_menu,
        "SessionLocal",
        return_value=session,
    ), patch.object(
        interview_menu,
        "InterviewService",
        return_value=interview_service,
    ), patch.object(
        interview_menu,
        "ExportService",
        return_value=exporter,
    ):
        interview_menu.export_interviews()

    exporter.export_interviews_to_csv.assert_called_once()