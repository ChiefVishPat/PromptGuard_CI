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
