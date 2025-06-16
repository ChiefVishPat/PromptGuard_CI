import xml.etree.ElementTree as ET

from typer.testing import CliRunner

from promptguard.cli import app


def test_integration_runner_and_reporter(tmp_path, monkeypatch):
    spec_content = """
tests:
  - name: pass_case
    prompt: foo
    checks:
      contains: foo
  - name: fail_case
    prompt: foo
    checks:
      contains: bar
"""
    spec_file = tmp_path / "spec.yml"
    spec_file.write_text(spec_content)
    monkeypatch.setattr("promptguard.runner.call_openai", lambda prompt: "foo")
    junit = tmp_path / "report.xml"
    runner = CliRunner()
    result = runner.invoke(app, ["test", str(spec_file), "-j", str(junit)])
    assert result.exit_code == 1
    root = ET.parse(str(junit)).getroot()
    assert root.attrib["tests"] == "2"
    assert root.attrib["failures"] == "1"
