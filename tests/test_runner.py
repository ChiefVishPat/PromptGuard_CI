import pytest

import promptguard.runner as runner_module
from promptguard.runner import Results, TestResult, run_tests


def test_run_tests_pass(monkeypatch):
    """
    When the model output contains the expected substring,
    run_tests should mark the test as passed with empty details.
    """
    spec = {
        "tests": [
            {
                "name": "check hello",
                "prompt": "Say hello",
                "checks": {"contains": "hello"},
            }
        ]
    }

    # stub out call_openai to return a predictable string
    monkeypatch.setattr(runner_module, "call_openai", lambda prompt: "hello world")
    results: Results = run_tests(spec)
    assert results.passed is True
    assert isinstance(results.test_results, list)

    tr: TestResult = results.test_results[0]
    assert tr.name == "check hello"
    assert tr.passed is True
    assert tr.details == ""


def test_run_tests_fail(monkeypatch):
    """
    When the model output does NOT contain the expected substring,
    run_tests should mark the test as failed and include the correct detail.
    """

    spec = {
        "tests": [{"name": "fail case", "prompt": "foo", "checks": {"contains": "bar"}}]
    }
    # Stub out call_openai to return a string missing "bar"
    monkeypatch.setattr(runner_module, "call_openai", lambda prompt: "Foo only")

    results: Results = run_tests(spec)
    assert results.passed is False

    tr: TestResult = results.test_results[0]
    assert tr.passed is False
    # The detail should match the runner's failure message
    assert "contains check failed: 'bar'" in tr.details


def test_run_tests_multiple_and_aggregate(monkeypatch):
    spec = {
        "tests": [
            {"name": "t1", "prompt": "p", "checks": {"contains": "x"}},
            {"name": "t2", "prompt": "p", "checks": {"contains": "y"}},
        ]
    }
    monkeypatch.setattr(runner_module, "call_openai", lambda prompt: "x")
    results = run_tests(spec)
    assert len(results.test_results) == 2
    assert results.passed is False


def test_run_tests_no_checks(monkeypatch):
    spec = {"tests": [{"name": "no_checks", "prompt": "p"}]}
    monkeypatch.setattr(runner_module, "call_openai", lambda prompt: "anything")
    results = run_tests(spec)
    tr = results.test_results[0]
    assert tr.passed is True
    assert tr.details == ""


def test_run_tests_multiple_checks_and_details(monkeypatch):
    spec = {
        "tests": [
            {
                "name": "multi",
                "prompt": "p",
                "checks": {"contains": "a", "not_contains": "b"},
            }
        ]
    }
    monkeypatch.setattr(runner_module, "call_openai", lambda prompt: "ab")
    results = run_tests(spec)
    tr = results.test_results[0]
    assert tr.passed is False
    assert "not_contains check failed: 'b'" in tr.details


def test_run_tests_json_and_toxicity_fail(monkeypatch):
    spec = {
        "tests": [
            {
                "name": "jt",
                "prompt": "p",
                "checks": {"json_valid": True, "toxicity": 0.3},
            }
        ]
    }
    monkeypatch.setattr(runner_module, "call_openai", lambda prompt: "not json")

    class Dummy:
        def __init__(self, api_key):
            pass

        def score(self, text):
            return {"TOXICITY": 0.5}

    monkeypatch.setattr("promptguard.checks.toxicity.PerspectiveAPI", Dummy)
    results = run_tests(spec)
    tr = results.test_results[0]
    assert tr.passed is False
    assert "json_valid check failed" in tr.details
    assert "toxicity check failed: score ≥ 0.3" in tr.details


def test_run_tests_unknown_check(monkeypatch):
    spec = {"tests": [{"name": "unknown", "prompt": "p", "checks": {"foo": "bar"}}]}
    monkeypatch.setattr(runner_module, "call_openai", lambda prompt: "anything")
    results = run_tests(spec)
    tr = results.test_results[0]
    assert tr.passed is True
    assert tr.details == ""


def test_run_tests_call_openai_raises(monkeypatch):
    spec = {"tests": [{"name": "err", "prompt": "p", "checks": {"contains": "a"}}]}
    monkeypatch.setattr(
        runner_module,
        "call_openai",
        lambda prompt: (_ for _ in ()).throw(RuntimeError("fail")),
    )
    with pytest.raises(RuntimeError):
        run_tests(spec)


def test_run_tests_invalid_toxicity_threshold(monkeypatch):
    spec = {
        "tests": [
            {"name": "bad_thresh", "prompt": "p", "checks": {"toxicity": "not_a_float"}}
        ]
    }
    monkeypatch.setattr(runner_module, "call_openai", lambda prompt: "anything")
    with pytest.raises(ValueError):
        run_tests(spec)
