from app.main import main


def test_main_exits_with_option_11(capsys, monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "11")

    main()

    captured = capsys.readouterr()

    assert "CAREERTRACK" in captured.out
    assert "Goodbye!" in captured.out