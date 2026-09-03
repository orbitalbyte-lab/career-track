from datetime import date
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from app.cli import application_menu


def make_company(
    company_id=1,
    name="Microsoft",
):
    return SimpleNamespace(
        id=company_id,
        name=name,
    )


def make_application(
    application_id=1,
    position="Software Engineer",
    company_id=1,
    company=None,
    application_type="Full-time",
    status="Applied",
    date_applied=date(2026, 8, 1),
    location="Seattle",
    deadline=date(2026, 9, 1),
    job_url="https://example.com/job",
    notes="Test application",
):
    if company is None:
        company = make_company(company_id)

    return SimpleNamespace(
        id=application_id,
        position=position,
        company_id=company_id,
        company=company,
        application_type=application_type,
        status=status,
        date_applied=date_applied,
        location=location,
        deadline=deadline,
        job_url=job_url,
        notes=notes,
    )


def test_add_application():
    application = make_application()

    session = MagicMock()
    service = MagicMock()
    service.create_application.return_value = application

    with (
        patch.object(
            application_menu,
            "SessionLocal",
            return_value=session,
        ),
        patch.object(
            application_menu,
            "ApplicationService",
            return_value=service,
        ),
        patch(
            "builtins.input",
            side_effect=[
                "1",
                "Software Engineer",
                "2",
                "2026-08-01",
                "2",
            ],
        ),
    ):
        application_menu.add_application()

    service.create_application.assert_called_once_with(
        company_id=1,
        position="Software Engineer",
        application_type="Full-time",
        date_applied=date(2026, 8, 1),
        status="Applied",
    )


def test_add_application_invalid_company_id(capsys):
    with patch(
        "builtins.input",
        return_value="abc",
    ):
        application_menu.add_application()

    output = capsys.readouterr().out

    assert "Company ID must be a number." in output


def test_add_application_invalid_type(capsys):
    with patch(
        "builtins.input",
        side_effect=[
            "1",
            "Software Engineer",
            "999",
        ],
    ):
        application_menu.add_application()

    output = capsys.readouterr().out

    assert "Invalid application type selection." in output


def test_add_application_invalid_date(capsys):
    with patch(
        "builtins.input",
        side_effect=[
            "1",
            "Software Engineer",
            "1",
            "wrong-date",
            "1",
        ],
    ):
        application_menu.add_application()

    output = capsys.readouterr().out

    assert "Invalid date. Use YYYY-MM-DD." in output


def test_add_application_invalid_status(capsys):
    with patch(
        "builtins.input",
        side_effect=[
            "1",
            "Software Engineer",
            "1",
            "2026-08-01",
            "999",
        ],
    ):
        application_menu.add_application()

    output = capsys.readouterr().out

    assert "Invalid status selection." in output


def test_add_application_handles_value_error(capsys):
    session = MagicMock()
    service = MagicMock()

    service.create_application.side_effect = ValueError("Company not found")

    with (
        patch.object(
            application_menu,
            "SessionLocal",
            return_value=session,
        ),
        patch.object(
            application_menu,
            "ApplicationService",
            return_value=service,
        ),
        patch(
            "builtins.input",
            side_effect=[
                "999",
                "Software Engineer",
                "1",
                "2026-08-01",
                "1",
            ],
        ),
    ):
        application_menu.add_application()

    output = capsys.readouterr().out

    assert "Error: Company not found" in output


def test_list_applications(capsys):
    applications = [
        make_application(
            application_id=1,
            position="Software Engineer",
        ),
        make_application(
            application_id=2,
            position="Data Analyst",
        ),
    ]

    session = MagicMock()
    service = MagicMock()
    service.get_applications.return_value = applications

    with (
        patch.object(
            application_menu,
            "SessionLocal",
            return_value=session,
        ),
        patch.object(
            application_menu,
            "ApplicationService",
            return_value=service,
        ),
    ):
        application_menu.list_applications()

    output = capsys.readouterr().out

    assert "Software Engineer" in output
    assert "Data Analyst" in output
    assert "Company ID: 1" in output
    assert "Status: Applied" in output


def test_list_applications_when_empty(capsys):
    session = MagicMock()
    service = MagicMock()
    service.get_applications.return_value = []

    with (
        patch.object(
            application_menu,
            "SessionLocal",
            return_value=session,
        ),
        patch.object(
            application_menu,
            "ApplicationService",
            return_value=service,
        ),
    ):
        application_menu.list_applications()

    output = capsys.readouterr().out

    assert "No applications found." in output


def test_sort_applications_by_date(capsys):
    applications = [
        make_application(
            position="Software Engineer",
        ),
    ]

    session = MagicMock()
    service = MagicMock()
    service.get_sorted_applications.return_value = applications

    with (
        patch.object(
            application_menu,
            "SessionLocal",
            return_value=session,
        ),
        patch.object(
            application_menu,
            "ApplicationService",
            return_value=service,
        ),
        patch(
            "builtins.input",
            return_value="1",
        ),
    ):
        application_menu.sort_applications()

    service.get_sorted_applications.assert_called_once_with("date")

    output = capsys.readouterr().out

    assert "Applications (Newest First)" in output
    assert "Software Engineer" in output


def test_sort_applications_by_position(capsys):
    session = MagicMock()
    service = MagicMock()
    service.get_sorted_applications.return_value = []

    with (
        patch.object(
            application_menu,
            "SessionLocal",
            return_value=session,
        ),
        patch.object(
            application_menu,
            "ApplicationService",
            return_value=service,
        ),
        patch(
            "builtins.input",
            return_value="2",
        ),
    ):
        application_menu.sort_applications()

    service.get_sorted_applications.assert_called_once_with("position")


def test_sort_applications_invalid_choice(capsys):
    with patch(
        "builtins.input",
        return_value="9",
    ):
        application_menu.sort_applications()

    output = capsys.readouterr().out

    assert "Invalid sorting option." in output


def test_view_application_invalid_id(capsys):
    with patch(
        "builtins.input",
        return_value="abc",
    ):
        application_menu.view_application()

    output = capsys.readouterr().out

    assert "Application ID must be a number." in output


def test_view_application_not_found(capsys):
    session = MagicMock()
    service = MagicMock()
    service.get_application.return_value = None

    with (
        patch.object(
            application_menu,
            "SessionLocal",
            return_value=session,
        ),
        patch.object(
            application_menu,
            "ApplicationService",
            return_value=service,
        ),
        patch(
            "builtins.input",
            return_value="999",
        ),
    ):
        application_menu.view_application()

    output = capsys.readouterr().out

    assert "Application not found." in output


def test_view_application(capsys):
    application = make_application()

    session = MagicMock()
    service = MagicMock()
    service.get_application.return_value = application

    with (
        patch.object(
            application_menu,
            "SessionLocal",
            return_value=session,
        ),
        patch.object(
            application_menu,
            "ApplicationService",
            return_value=service,
        ),
        patch(
            "builtins.input",
            return_value="1",
        ),
    ):
        application_menu.view_application()

    output = capsys.readouterr().out

    assert "Application Details" in output
    assert "Microsoft" in output
    assert "Software Engineer" in output
    assert "Full-time" in output
    assert "Applied" in output
    assert "Seattle" in output


def test_update_application_invalid_id(capsys):
    with patch(
        "builtins.input",
        return_value="abc",
    ):
        application_menu.update_application()

    output = capsys.readouterr().out

    assert "Application ID must be a number." in output


def test_update_application_not_found(capsys):
    session = MagicMock()
    service = MagicMock()
    service.get_application.return_value = None

    with (
        patch.object(
            application_menu,
            "SessionLocal",
            return_value=session,
        ),
        patch.object(
            application_menu,
            "ApplicationService",
            return_value=service,
        ),
        patch(
            "builtins.input",
            return_value="999",
        ),
    ):
        application_menu.update_application()

    output = capsys.readouterr().out

    assert "Application not found." in output


def test_update_application(capsys):
    application = make_application()

    updated_application = make_application(
        position="Senior Software Engineer",
        status="Interview",
        location="California",
        deadline=date(2026, 9, 15),
        job_url="https://google.com/job",
        notes="Updated notes",
    )

    session = MagicMock()
    service = MagicMock()

    service.get_application.return_value = application
    service.update_application.return_value = updated_application

    with (
        patch.object(
            application_menu,
            "SessionLocal",
            return_value=session,
        ),
        patch.object(
            application_menu,
            "ApplicationService",
            return_value=service,
        ),
        patch(
            "builtins.input",
            side_effect=[
                "1",
                "Senior Software Engineer",
                "Interview",
                "California",
                "2026-09-15",
                "https://google.com/job",
                "Updated notes",
            ],
        ),
    ):
        application_menu.update_application()

    service.update_application.assert_called_once_with(
        application_id=1,
        position="Senior Software Engineer",
        status="Interview",
        location="California",
        deadline=date(2026, 9, 15),
        job_url="https://google.com/job",
        notes="Updated notes",
    )

    output = capsys.readouterr().out

    assert "Application updated successfully!" in output


def test_update_application_invalid_deadline(capsys):
    application = make_application()

    session = MagicMock()
    service = MagicMock()
    service.get_application.return_value = application

    with (
        patch.object(
            application_menu,
            "SessionLocal",
            return_value=session,
        ),
        patch.object(
            application_menu,
            "ApplicationService",
            return_value=service,
        ),
        patch(
            "builtins.input",
            side_effect=[
                "1",
                "",
                "",
                "",
                "wrong-date",
                "",
                "",
            ],
        ),
    ):
        application_menu.update_application()

    output = capsys.readouterr().out

    assert "Invalid deadline. Use YYYY-MM-DD." in output


def test_update_application_handles_value_error(capsys):
    application = make_application()

    session = MagicMock()
    service = MagicMock()

    service.get_application.return_value = application
    service.update_application.side_effect = ValueError(
        "Deadline cannot be before the application date"
    )

    with (
        patch.object(
            application_menu,
            "SessionLocal",
            return_value=session,
        ),
        patch.object(
            application_menu,
            "ApplicationService",
            return_value=service,
        ),
        patch(
            "builtins.input",
            side_effect=[
                "1",
                "",
                "",
                "",
                "2026-07-01",
                "",
                "",
            ],
        ),
    ):
        application_menu.update_application()

    output = capsys.readouterr().out

    assert "Error: Deadline cannot be before the application date" in output


def test_search_applications_empty_query(capsys):
    with patch(
        "builtins.input",
        return_value="   ",
    ):
        application_menu.search_applications()

    output = capsys.readouterr().out

    assert "Search query cannot be empty." in output


def test_search_applications(capsys):
    applications = [
        make_application(
            position="Software Engineer",
        ),
    ]

    session = MagicMock()
    service = MagicMock()
    service.search_applications.return_value = applications

    with (
        patch.object(
            application_menu,
            "SessionLocal",
            return_value=session,
        ),
        patch.object(
            application_menu,
            "ApplicationService",
            return_value=service,
        ),
        patch(
            "builtins.input",
            return_value="Software",
        ),
    ):
        application_menu.search_applications()

    service.search_applications.assert_called_once_with("Software")

    output = capsys.readouterr().out

    assert "Search results for 'Software':" in output
    assert "Software Engineer" in output


def test_search_applications_no_results(capsys):
    session = MagicMock()
    service = MagicMock()
    service.search_applications.return_value = []

    with (
        patch.object(
            application_menu,
            "SessionLocal",
            return_value=session,
        ),
        patch.object(
            application_menu,
            "ApplicationService",
            return_value=service,
        ),
        patch(
            "builtins.input",
            return_value="Unknown",
        ),
    ):
        application_menu.search_applications()

    output = capsys.readouterr().out

    assert "No applications found." in output


def test_filter_applications(capsys):
    applications = [
        make_application(),
    ]

    session = MagicMock()
    service = MagicMock()
    service.filter_applications.return_value = applications

    with (
        patch.object(
            application_menu,
            "SessionLocal",
            return_value=session,
        ),
        patch.object(
            application_menu,
            "ApplicationService",
            return_value=service,
        ),
        patch(
            "builtins.input",
            side_effect=[
                "Applied",
                "Full-time",
                "1",
            ],
        ),
    ):
        application_menu.filter_applications()

    service.filter_applications.assert_called_once_with(
        status="Applied",
        application_type="Full-time",
        company_id=1,
    )

    output = capsys.readouterr().out

    assert "Filtered Applications" in output
    assert "Total results: 1" in output


def test_filter_applications_invalid_company_id(capsys):
    with patch(
        "builtins.input",
        side_effect=[
            "",
            "",
            "abc",
        ],
    ):
        application_menu.filter_applications()

    output = capsys.readouterr().out

    assert "Company ID must be a number." in output


def test_filter_applications_without_filter(capsys):
    with patch(
        "builtins.input",
        side_effect=[
            "",
            "",
            "",
        ],
    ):
        application_menu.filter_applications()

    output = capsys.readouterr().out

    assert "Please provide at least one filter." in output


def test_filter_applications_no_results(capsys):
    session = MagicMock()
    service = MagicMock()
    service.filter_applications.return_value = []

    with (
        patch.object(
            application_menu,
            "SessionLocal",
            return_value=session,
        ),
        patch.object(
            application_menu,
            "ApplicationService",
            return_value=service,
        ),
        patch(
            "builtins.input",
            side_effect=[
                "Applied",
                "",
                "",
            ],
        ),
    ):
        application_menu.filter_applications()

    output = capsys.readouterr().out

    assert "No applications found." in output


def test_delete_application_invalid_id(capsys):
    with patch(
        "builtins.input",
        return_value="abc",
    ):
        application_menu.delete_application()

    output = capsys.readouterr().out

    assert "Application ID must be a number." in output


def test_delete_application_not_found(capsys):
    session = MagicMock()
    service = MagicMock()
    service.get_application.return_value = None

    with (
        patch.object(
            application_menu,
            "SessionLocal",
            return_value=session,
        ),
        patch.object(
            application_menu,
            "ApplicationService",
            return_value=service,
        ),
        patch(
            "builtins.input",
            return_value="999",
        ),
    ):
        application_menu.delete_application()

    output = capsys.readouterr().out

    assert "Application not found." in output


def test_delete_application_cancelled(capsys):
    application = make_application()

    session = MagicMock()
    service = MagicMock()
    service.get_application.return_value = application

    with (
        patch.object(
            application_menu,
            "SessionLocal",
            return_value=session,
        ),
        patch.object(
            application_menu,
            "ApplicationService",
            return_value=service,
        ),
        patch(
            "builtins.input",
            side_effect=[
                "1",
                "n",
            ],
        ),
    ):
        application_menu.delete_application()

    service.delete_application.assert_not_called()

    output = capsys.readouterr().out

    assert "Deletion cancelled." in output


def test_delete_application(capsys):
    application = make_application()

    session = MagicMock()
    service = MagicMock()

    service.get_application.return_value = application
    service.delete_application.return_value = True

    with (
        patch.object(
            application_menu,
            "SessionLocal",
            return_value=session,
        ),
        patch.object(
            application_menu,
            "ApplicationService",
            return_value=service,
        ),
        patch(
            "builtins.input",
            side_effect=[
                "1",
                "y",
            ],
        ),
    ):
        application_menu.delete_application()

    service.delete_application.assert_called_once_with(1)

    output = capsys.readouterr().out

    assert "Application deleted successfully!" in output


def test_delete_application_when_delete_fails(capsys):
    application = make_application()

    session = MagicMock()
    service = MagicMock()

    service.get_application.return_value = application
    service.delete_application.return_value = False

    with (
        patch.object(
            application_menu,
            "SessionLocal",
            return_value=session,
        ),
        patch.object(
            application_menu,
            "ApplicationService",
            return_value=service,
        ),
        patch(
            "builtins.input",
            side_effect=[
                "1",
                "y",
            ],
        ),
    ):
        application_menu.delete_application()

    output = capsys.readouterr().out

    assert "Application not found." in output


def test_show_dashboard(capsys):
    session = MagicMock()

    application_service = MagicMock()
    application_service.get_dashboard_statistics.return_value = {
        "total": 10,
        "total_companies": 5,
        "success_rate": 20.0,
        "by_status": {
            "Applied": 6,
            "Interview": 2,
            "Rejected": 2,
        },
        "by_application_type": {
            "Full-time": 7,
            "Internship": 3,
        },
        "by_company": {
            "Microsoft": 4,
            "Google": 3,
        },
    }

    application_service.get_monthly_application_counts.return_value = {
        "2026-07": 4,
        "2026-08": 6,
    }

    application_service.get_location_statistics.return_value = {
        "Seattle": 5,
        "Remote": 5,
    }

    application_service.get_recent_applications.return_value = []

    application_service.get_upcoming_deadlines.return_value = []

    interview_service = MagicMock()

    interview_service.get_interview_statistics.return_value = {
        "Interview": 2,
    }

    interview_service.get_interview_analytics.return_value = {
        "total": 2,
        "completed": 1,
        "cancelled": 0,
        "passed": 1,
        "failed": 0,
        "pending": 1,
        "online": 1,
        "phone": 1,
        "on_site": 0,
    }

    interview_service.get_upcoming_interviews.return_value = []

    interview_service.get_this_week_interviews.return_value = []

    follow_up_service = MagicMock()

    follow_up_service.get_follow_up_statistics.return_value = {
        "total": 3,
        "completed": 1,
        "pending": 2,
    }

    follow_up_service.get_upcoming_follow_ups.return_value = []

    with (
        patch.object(
            application_menu,
            "SessionLocal",
            return_value=session,
        ),
        patch.object(
            application_menu,
            "ApplicationService",
            return_value=application_service,
        ),
        patch.object(
            application_menu,
            "InterviewService",
            return_value=interview_service,
        ),
        patch.object(
            application_menu,
            "FollowUpService",
            return_value=follow_up_service,
        ),
    ):
        application_menu.show_dashboard()

    output = capsys.readouterr().out

    assert "CareerTrack Dashboard" in output
    assert "Total Applications" in output
    assert "10" in output
    assert "Total Companies" in output
    assert "5" in output
    assert "Success Rate" in output
    assert "20.0%" in output
    assert "Applications by Status" in output
    assert "Applications by Type" in output
    assert "Applications by Company" in output
    assert "Applications by Month" in output
    assert "Applications by Location" in output
    assert "Recent Applications" in output
    assert "Upcoming Deadlines" in output
    assert "Interview Statistics" in output
    assert "Interview Analytics" in output
    assert "Upcoming Interviews" in output
    assert "Interviews This Week" in output
    assert "Follow-Up Statistics" in output
    assert "Upcoming Follow-Ups" in output


def test_export_applications(capsys):
    session = MagicMock()

    application_service = MagicMock()

    exporter = MagicMock()
    exporter.export_applications_to_csv.return_value = "exports/applications.csv"

    with (
        patch.object(
            application_menu,
            "SessionLocal",
            return_value=session,
        ),
        patch.object(
            application_menu,
            "ApplicationService",
            return_value=application_service,
        ),
        patch.object(
            application_menu,
            "ExportService",
            return_value=exporter,
        ),
    ):
        application_menu.export_applications()

    exporter.export_applications_to_csv.assert_called_once()

    output = capsys.readouterr().out

    assert "Export Applications" in output
    assert "Applications exported to: exports/applications.csv" in output


def test_import_applications(capsys):
    session = MagicMock()

    application_service = MagicMock()

    importer = MagicMock()

    importer.import_applications_from_csv.return_value = [
        {"position": "Software Engineer"},
        {"position": "Backend Developer"},
    ]

    with (
        patch.object(
            application_menu,
            "SessionLocal",
            return_value=session,
        ),
        patch.object(
            application_menu,
            "ApplicationService",
            return_value=application_service,
        ),
        patch.object(
            application_menu,
            "ImportService",
            return_value=importer,
        ),
        patch(
            "builtins.input",
            return_value="applications.csv",
        ),
    ):
        application_menu.import_applications()

    importer.import_applications_from_csv.assert_called_once_with("applications.csv")

    output = capsys.readouterr().out

    assert "Import Applications" in output
    assert "Imported 2 applications." in output
