import logging
import ssl
from pathlib import Path

import certifi
import typer
from dotenv import load_dotenv

from promptguard.loader import load_spec
from promptguard.logging_config import setup_logging
from promptguard.reporter import write_junit
from promptguard.runner import Results, run_tests

# Ensure proper SSL certificate bundle on macOS (e.g. for Perspective API)
ssl._create_default_https_context = lambda *args, **kwargs: ssl.create_default_context(
    cafile=certifi.where()
)

project_root = Path(__file__).parent.parent
dotenv_path = project_root / ".env"
load_dotenv(dotenv_path)

setup_logging(level=logging.DEBUG)
logger = logging.getLogger(__name__)
app = typer.Typer(help="PromptGuard CI CLI")


@app.callback()
def main() -> None:
    """PromptGuard command line interface."""
    pass


@app.command(
    "test",
    help=(
        "Run promptguard tests defined in a YAML spec file or a directory of specs, "
        "then optionally emit JUnit XML."
    ),
)
def test_command(
    spec: str = typer.Argument(
        ..., help="Path to a YAML test spec file or a directory containing specs"
    ),
    junit_output: str = typer.Option(
        None,
        "--junit-output",
        "-j",
        help="Where to write the JUnit XML report",
    ),
):
    logger.info(
        "Starting 'test' command with spec=%s junit_output=%s", spec, junit_output
    )
    spec_path = Path(spec)
    test_results = []
    if spec_path.is_dir():
        spec_files = sorted(spec_path.glob("*.yml")) + sorted(spec_path.glob("*.yaml"))
        if not spec_files:
            raise typer.BadParameter(f"No YAML spec files found in directory {spec}")
        for spec_file in spec_files:
            spec_dict = load_spec(str(spec_file))
            results = run_tests(spec_dict)
            for tr in results.test_results:
                tr.name = f"{spec_file.name}:{tr.name}"
            test_results.extend(results.test_results)
        results = Results(test_results)
    else:
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
