import re
import xml.etree.ElementTree as ET

from promptguard.reporter import write_junit
from promptguard.runner import Results, TestResult


def test_write_junit_minial(tmp_path):
    # 1) Prepare Results: one pass, one fail
    tr_pass = TestResult(name="pass_case", passed=True, details="")
    tr_fail = TestResult(name="fail_case", passed=False, details="oops")
    results = Results(test_results=[tr_pass, tr_fail])

    # 2) Write to 'test_report.xml'
    xml_path = tmp_path / "test_report.xml"
    write_junit(results=results, path=str(xml_path))
    assert xml_path.exists()

    # 3) Parse and assert structure
    root = ET.parse(str(xml_path)).getroot()
    assert root.tag == "testsuite"

    # Suite attributes
    assert root.attrib["name"] == "PromptGuard Tests"
    assert root.attrib["tests"] == "2"
    assert root.attrib["failures"] == "1"
    assert "time" in root.attrib

    # properties block
    props = root.find("properties")
    assert props is not None
    prop_names = {p.attrib["name"] for p in props.findall("property")}
    assert "generatedBy" in prop_names
    assert "timestamp" in prop_names

    # testcase elements
    tcs = list(root.findall("testcase"))
    assert len(tcs) == 2

    # Check classname on each testcase
    for tc in tcs:
        assert tc.attrib["classname"] == "promptguard.runner"

    # Passing testcase has no <failure>
    tc1 = next(tc for tc in tcs if tc.attrib["name"] == "pass_case")
    assert tc1.find("failure") is None

    # Failing testcase has a <failure> with correct message/text
    tc2 = next(tc for tc in tcs if tc.attrib["name"] == "fail_case")
    f = tc2.find("failure")
    assert f is not None
    assert f.attrib["message"] == "oops"
    assert f.text == "oops"


def test_write_junit_empty(tmp_path):
    # Zero tests => tests="0", failures="0"
    results = Results(test_results=[])
    xml_path = tmp_path / "test_report.xml"
    write_junit(results, str(xml_path))
    root = ET.parse(str(xml_path)).getroot()
    assert root.attrib["tests"] == "0"
    assert root.attrib["failures"] == "0"
    # Should still have properties
    assert root.find("properties") is not None


def test_write_junit_xml_declaration_and_timing(tmp_path):
    from promptguard.runner import Results, TestResult

    xml_path = tmp_path / "test_report.xml"
    tr = TestResult(name="f", passed=False, details="oops <&> '\"")
    results = Results(test_results=[tr])
    write_junit(results, str(xml_path))
    content = xml_path.read_text(encoding="utf-8")
    assert content.startswith('<?xml version="1.0" encoding="utf-8"?>')
    # time attribute should be on the second line's testsuite element
    second_line = content.splitlines()[1]
    assert 'time="' in second_line and re.search(r'time="\d+\.\d{3}"', second_line)


def test_write_junit_timestamp_format(tmp_path):
    xml_path = tmp_path / "test_report.xml"
    from promptguard.runner import Results, TestResult

    tr = TestResult(name="p", passed=True, details="")
    results = Results(test_results=[tr])
    write_junit(results, str(xml_path))
    root = ET.parse(str(xml_path)).getroot()
    props = root.find("properties")
    timestamp = [
        p.attrib["value"]
        for p in props.findall("property")
        if p.attrib["name"] == "timestamp"
    ][0]
    assert re.match(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z$", timestamp)
