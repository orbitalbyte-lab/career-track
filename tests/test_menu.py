from unittest.mock import patch

from app.cli.menu import run


def test_run_dispatches_all_menu_options(monkeypatch):
    options = [
        ("1", "add_company"),
        ("2", "list_companies"),
        ("3", "view_company"),
        ("4", "update_company"),
        ("5", "delete_company"),
        ("6", "search_companies"),
        ("7", "add_application"),
        ("8", "list_applications"),
        ("9", "view_application"),
        ("10", "update_application"),
        ("11", "delete_application"),
        ("12", "search_applications"),
        ("13", "show_dashboard"),
        ("14", "filter_applications"),
        ("15", "export_applications"),
        ("16", "sort_applications"),
        ("17", "import_applications"),
        ("18", "export_interviews"),
        ("19", "add_interview"),
        ("20", "list_interviews"),
        ("21", "view_interview"),
        ("22", "update_interview"),
        ("23", "delete_interview"),
        ("24", "search_interviews"),
        ("25", "filter_interviews"),
        ("26", "sort_interviews"),
        ("27", "add_follow_up"),
        ("28", "list_follow_ups"),
        ("29", "view_follow_up"),
        ("30", "complete_follow_up"),
        ("31", "reopen_follow_up"),
        ("32", "delete_follow_up"),
        ("33", "upcoming_follow_ups"),
        ("34", "list_pending_follow_ups"),
        ("35", "list_completed_follow_ups"),
    ]

    inputs = iter([option for option, _ in options] + ["36"])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs),
    )

    patch_targets = {
        function_name: patch(
            f"app.cli.menu.{function_name}"
        )
        for _, function_name in options
    }

    mocked_functions = {}

    for function_name, patcher in patch_targets.items():
        mocked_functions[function_name] = patcher.start()

    try:
        run()
    finally:
        for patcher in patch_targets.values():
            patcher.stop()

    for _, function_name in options:
        mocked_functions[function_name].assert_called_once()


def test_run_handles_invalid_option(
    capsys,
    monkeypatch,
):
    inputs = iter(["999", "36"])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs),
    )

    run()

    captured = capsys.readouterr()

    assert "Invalid option. Please try again." in captured.out


def test_show_menu_displays_all_options(capsys):
    from app.cli.menu import show_menu

    show_menu()

    captured = capsys.readouterr()

    for option in range(1, 37):
        assert f"{option}." in captured.out

    assert "CAREERTRACK" in captured.out