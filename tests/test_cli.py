from commandgraph.cli import main


def test_explain_known_command_json(capsys):
    exit_code = main(["explain", "chmod", "--json"])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert '"schema_version": "commandgraph.command_card.v1"' in captured.out
    assert '"command": "chmod"' in captured.out


def test_doctor_passes(capsys):
    exit_code = main(["doctor"])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "ok: true" in captured.out


def test_doctor_has_seed_command_coverage():
    from commandgraph.data import data_health

    health = data_health()
    assert health["command_count"] >= 30
