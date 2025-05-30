from typer.testing import CliRunner

from promptguard.cli import app

runner = CliRunner()


def test_help_shows_usage():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Usage:" in result.stdout
    assert "promptguard" in result.stdout.lower()
