from app.main import main


def test_main_exits_with_option_17(
    capsys,
    monkeypatch,
):
    monkeypatch.setattr(
        "builtins.input",
        lambda _: "17",
    )

    main()

    captured = capsys.readouterr()

    assert "CAREERTRACK" in captured.out
    assert "Goodbye!" in captured.out


def test_main_dashboard_option(
    capsys,
    monkeypatch,
):
    inputs = iter(
        ["13", "17"]
    )

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs),
    )

    main()

    captured = capsys.readouterr()

    assert "CAREERTRACK" in captured.out
    assert "Total Applications" in captured.out
    assert "Applications by Status" in captured.out
    assert "Applications by Type" in captured.out
    assert "Applications by Company" in captured.out
    assert "Upcoming Deadlines" in captured.out
    assert "Goodbye!" in captured.out