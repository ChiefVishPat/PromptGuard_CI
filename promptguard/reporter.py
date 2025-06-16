import logging
import time
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

from promptguard.runner import Results

logger = logging.getLogger(__name__)


def write_junit(results: Results, path: str) -> None:
    """
    Write a JUnit XML report to `path`, including:
      - testsuite attributes: name, tests, failures, time
      - a <properties> block with generator and timestamp
      - each testcase with classname and a placeholder time
    """
    logger.info(
        f"Writing JUnit report to {path} with {len(results.test_results)} testcases"
    )
    start_time = time.perf_counter()
    # Create <testsuite> root with counts
    tests = len(results.test_results)
    failures = sum(1 for t in results.test_results if not t.passed)
    suite = ET.Element(
        "testsuite",
        attrib={
            "name": "PromptGuard Tests",
            "tests": str(tests),
            "failures": str(failures),
        },
    )

    # Add properties to the elements
    props = ET.SubElement(suite, "properties")
    ET.SubElement(
        props, "property", attrib={"name": "generatedBy", "value": "PromptGuard CI"}
    )
    ET.SubElement(
        props,
        "property",
        attrib={
            "name": "timestamp",
            "value": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        },
    )

    # A simple stub: one <testcase> per TestResult
    for tr in results.test_results:
        tc = ET.SubElement(
            suite,
            "testcase",
            attrib={"classname": "promptguard.runner", "name": tr.name},
        )
        if not tr.passed:
            failure = ET.SubElement(
                tc, "failure", attrib={"message": tr.details or "failed"}
            )
            failure.text = tr.details

    # Compute total elapsed time and set on testsuite
    elapsed = time.perf_counter() - start_time
    suite.set("time", f"{elapsed:.3f}")

    # Write to disk with XML declaration
    tree = ET.ElementTree(suite)
    # Write XML declaration with double quotes, then the rest of the document
    with open(path, "wb") as f:
        f.write(b'<?xml version="1.0" encoding="utf-8"?>\n')
        tree.write(f, encoding="utf-8", xml_declaration=False)
    logger.info(f"JUnit report written to {path} (total time: {elapsed:.3f}s)")
