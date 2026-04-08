from core.db.migrations import run_migrations


def test_run_migrations_uses_alembic(monkeypatch):
    captured = {}

    def fake_upgrade(config, revision):
        captured["config_file_name"] = config.config_file_name
        captured["revision"] = revision

    monkeypatch.setattr("core.db.migrations.command.upgrade", fake_upgrade)

    run_migrations()

    assert captured["config_file_name"].endswith("alembic.ini")
    assert captured["revision"] == "head"
