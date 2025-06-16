from promptguard.checks.contains import check_contains
from promptguard.checks.json_valid import check_json_valid
from promptguard.checks.not_contains import check_not_contains
from promptguard.checks.toxicity import check_toxicity


def test_contains_positive():
    assert check_contains("hello world", "world")


def test_contains_negative():
    assert not check_contains("foo", "bar")


def test_not_contains_positive():
    assert check_not_contains("foo", "bar")


def test_not_contains_negative():
    assert not check_not_contains("hello", "hello")


def test_json_valid_positive():
    assert check_json_valid('{"a": 1, "b": []}')


def test_json_valid_negative():
    assert not check_json_valid("this is not json")


def test_toxicity_threshold(monkeypatch):
    """
    Stub out the PerspectiveAPI so we can control the toxicity score.
    """

    class DummyClient:
        def __init__(self, api_key):
            # api_key is ignored
            pass

        def score(self, text):
            # always return 0.4 for TOXICITY
            return {"TOXICITY": 0.4}

    # Replace the real PerspectiveAPI with our dummy
    monkeypatch.setattr("promptguard.checks.toxicity.PerspectiveAPI", DummyClient)

    # Below threshold => passes
    assert check_toxicity("anything", threshold=0.5)
    # Above threshold => fails
    assert not check_toxicity("anything", threshold=0.3)


def test_contains_positions_and_case_sensitivity():
    text = "Foobar baz"
    assert check_contains(text, "Foo")
    assert check_contains(text, "bar")
    assert check_contains(text, "baz")
    assert not check_contains(text, "foo")
    assert not check_contains(text, "qux")


def test_contains_empty_substring():
    assert check_contains("anything", "")
    assert not check_not_contains("anything", "")


def test_json_valid_various_types_and_edge_cases():
    assert check_json_valid("[]")
    assert check_json_valid('[1, 2, "a"]')
    assert check_json_valid("123")
    assert check_json_valid("3.14")
    nested = '{"a": {"b": [1, {"c": "ö"}]}}'
    assert check_json_valid(nested)
    assert not check_json_valid("")
    assert not check_json_valid("   ")


def test_toxicity_boundary_conditions(monkeypatch):
    class Dummy:
        def __init__(self, api_key):
            pass

        def score(self, text):
            return {"TOXICITY": 0.5}

    monkeypatch.setattr("promptguard.checks.toxicity.PerspectiveAPI", Dummy)
    assert not check_toxicity("anything", threshold=0.5)

    class DummyZero:
        def __init__(self, api_key):
            pass

        def score(self, text):
            return {"TOXICITY": 0.0}

    monkeypatch.setattr("promptguard.checks.toxicity.PerspectiveAPI", DummyZero)
    assert not check_toxicity("anything", threshold=0.0)

    class DummyBelowOne:
        def __init__(self, api_key):
            pass

        def score(self, text):
            return {"TOXICITY": 0.999}

    monkeypatch.setattr("promptguard.checks.toxicity.PerspectiveAPI", DummyBelowOne)
    assert check_toxicity("anything", threshold=1.0)
