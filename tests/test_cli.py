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
    # Should show a usage line for the 'test' command
    assert "Usage:" in output
    # Should document the SPEC argument
    assert "SPEC" in output
    # Should list the --junit-output option (and its short form)
    assert "--junit-output" in output
    assert "-j" in output
