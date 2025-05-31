import logging
from pathlib import Path

import typer
from dotenv import load_dotenv

from promptguard.loader import load_spec
from promptguard.logging_config import setup_logging
from promptguard.reporter import write_junit
from promptguard.runner import run_tests

project_root = Path(__file__).parent.parent
dotenv_path = project_root / ".env"
load_dotenv(dotenv_path)  # <-- this reads .env into os.environ

setup_logging(level=logging.DEBUG)

logger = logging.getLogger(__name__)
app = typer.Typer()


@app.command()
def test(
    spec: str = typer.Argument(..., help="Path to your YAML test spec"),
    junit_output: str = typer.Option(
        None, "--junit-output", "-j", help="Where to write the JUnit XML report"
    ),
):
    """
    Run promptguard tests defined in a YAML spec, then optionally emit JUnit XML.
    """
    logger.info(
        "Starting 'test' command with spec=%s junit_output=%s", spec, junit_output
    )
    spec_dict = load_spec(spec)
    results = run_tests(spec_dict)
    if junit_output:
        write_junit(results, junit_output)
        logger.info("Wrote JUnit report to %s", junit_output)
    exit_code = 0 if results.passed else 1
    logger.info("Exiting with code %d (all passed? %s)", exit_code, results.passed)
    raise typer.Exit(code=exit_code)


if __name__ == "__main__":
    app()
