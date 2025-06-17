import logging
import os
from dataclasses import dataclass
from typing import Any, Dict, List

from openai import OpenAI

from promptguard.checks.contains import check_contains
from promptguard.checks.json_valid import check_json_valid
from promptguard.checks.not_contains import check_not_contains
from promptguard.checks.toxicity import check_toxicity

logger = logging.getLogger(__name__)


@dataclass
class TestResult:
    """Result of a single test case"""

    # Prevent pytest from collecting this dataclass as a test case
    __test__ = False

    name: str
    passed: bool
    details: str = ""


@dataclass
class Results:
    """Aggregrated test results"""

    test_results: List[TestResult]

    @property
    def passed(self) -> bool:
        """Overall pass if no individual failures"""
        return all(tr.passed for tr in self.test_results)


def call_openai(prompt: str) -> str:
    """
    Send a prompt to the OpenAI chat model (gpt-4o-mini)
    and return the assistant's reply text.
    """
    api_key = os.getenv("OPENAI_API_KEY", "")
    logger.debug(f"Initializing OpenAI client (key set? {'yes' if api_key else 'no'})")
    try:
        client = OpenAI(api_key=api_key)
        logger.debug(f"Sending chat request to gpt-4o-mini with prompt={prompt!r}")
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=50,
            temperature=0.0,
        )
        content = resp.choices[0].message.content
        logger.debug(f"gpt-4o-mini replied: {content!r}")
        return content
    except Exception as e:
        logger.error(f"OpenAI API error: {e}")
        raise RuntimeError(f"OpenAI API error: {e}") from e


def run_tests(spec: Dict[str, Any]) -> Results:
    """
    Execute all tests defined in the spec.
    Supported checks: contains, not_contains, json_valid, toxicity.
    """
    tests = spec.get("tests", [])
    logger.info(f"Running {len(tests)} tests from spec")
    results: List[TestResult] = []

    for idx, t in enumerate(tests, start=1):
        name = t["name"]
        prompt = t["prompt"]
        checks = t.get("checks", {})

        logger.info(f"Test {idx}/{len(tests)}: {name}")
        output = call_openai(prompt=prompt)

        passed = True
        details: List[str] = []

        if "contains" in checks:
            substring = checks["contains"]
            ok = check_contains(output=output, substring=substring)
            logger.debug(f"contains check for {substring!r} => {ok}")
            passed &= ok
            if not ok:
                details.append(f"contains check failed: {substring!r}")

        if "not_contains" in checks:
            substring = checks["not_contains"]
            ok = check_not_contains(output, substring)
            logger.debug(f"not_contains check for {substring!r} => {ok}")
            passed &= ok
            if not ok:
                details.append(f"not_contains check failed: {substring!r}")

        if checks.get("json_valid", False):
            ok = check_json_valid(output)
            logger.debug(f"json_valid check => {ok}")
            passed &= ok
            if not ok:
                details.append("json_valid check failed")

        if "toxicity" in checks:
            threshold = float(checks["toxicity"])
            ok = check_toxicity(output, threshold)
            logger.debug(f"toxicity check < {threshold} => {ok}")
            passed &= ok
            if not ok:
                details.append(f"toxicity check failed: score ≥ {threshold}")

        detail_str = "; ".join(details)
        logger.info(
            f"Test {idx}/{len(tests)} '{name}' completed: passed={passed}"
            + (f", details={detail_str}" if detail_str else "")
        )
        results.append(TestResult(name=name, passed=passed, details=detail_str))

    return Results(results)
