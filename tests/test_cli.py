from pathlib import Path

from click.utils import strip_ansi
from typer.testing import CliRunner

from promptguard.cli import app

runner = CliRunner()


def test_root_help_shows_usage_and_commands():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    output = result.stdout.lower()
    # Check that it shows a usage line
    assert "usage:" in output
    # The 'test' command should be listed
    assert "test" in output


def test_test_command_help_shows_spec_and_options():
    result = runner.invoke(app, ["test", "--help"], color=False)
    assert result.exit_code == 0
    output = result.stdout
    output = strip_ansi(result.stdout)
    # Should show a usage line for the 'test' command
    assert "Usage:" in output
    # Should document the SPEC argument
    assert "SPEC" in output
    # Should list the --junit-output option (and its short form)
    assert "--junit-output" in output
    assert "-j" in output


def test_cli_happy_path_writes_file(tmp_path, monkeypatch):
    spec_file = tmp_path / "spec.yml"
    spec_file.write_text("tests: []")
    junit_file = tmp_path / "out.xml"
    monkeypatch.setattr("promptguard.cli.load_spec", lambda p: {"tests": []})

    class DummyResults:
        passed = True

    monkeypatch.setattr("promptguard.cli.run_tests", lambda spec: DummyResults())

    def fake_write(results, path):
        Path(path).write_text("dummy")

    monkeypatch.setattr("promptguard.cli.write_junit", fake_write)
    result = runner.invoke(app, ["test", str(spec_file), "-j", str(junit_file)])
    assert result.exit_code == 0
    assert junit_file.exists()


def test_cli_fail_path_exit_code(tmp_path, monkeypatch):
    spec_file = tmp_path / "spec.yml"
    spec_file.write_text("tests: []")
    monkeypatch.setattr("promptguard.cli.load_spec", lambda p: {"tests": []})

    class DummyResults:
        passed = False

    monkeypatch.setattr("promptguard.cli.run_tests", lambda spec: DummyResults())
    monkeypatch.setattr("promptguard.cli.write_junit", lambda r, p: None)
    result = runner.invoke(app, ["test", str(spec_file), "-j", "dummy"])
    assert result.exit_code == 1


def test_cli_no_junit_output(tmp_path, monkeypatch):
    spec_file = tmp_path / "spec.yml"
    spec_file.write_text("tests: []")
    monkeypatch.setattr("promptguard.cli.load_spec", lambda p: {"tests": []})

    class DummyResults:
        passed = True

    monkeypatch.setattr("promptguard.cli.run_tests", lambda spec: DummyResults())
    result = runner.invoke(app, ["test", str(spec_file)])
    assert result.exit_code == 0


def test_cli_load_spec_raises(tmp_path, monkeypatch):
    spec_file = tmp_path / "spec.yml"
    spec_file.write_text("bad")

    def bad_load(p):
        raise ValueError("bad")

    monkeypatch.setattr("promptguard.cli.load_spec", bad_load)
    result = runner.invoke(app, ["test", str(spec_file)])
    assert result.exit_code != 0


def test_cli_invalid_option_shows_usage():
    result = runner.invoke(app, ["--unknown"])
    assert result.exit_code != 0
    output = (result.stdout or "") + (getattr(result, "stderr", "") or "")
    assert "Usage" in output
