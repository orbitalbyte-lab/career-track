from app.main import main


def test_main(capsys, monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "5")

    main()

    captured = capsys.readouterr()

    assert "CAREERTRACK" in captured.out
    assert "Goodbye!" in captured.out