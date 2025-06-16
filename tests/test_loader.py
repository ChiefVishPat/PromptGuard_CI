import os

import pytest

from promptguard.loader import load_spec


def test_load_hello_spec(tmp_path):
    # Copy the example file into a temp directory
    src = os.path.join(os.path.dirname(__file__), "../examples/hello.yml")
    dest = tmp_path / "hello.yml"
    dest.write_text(open(src, "r", encoding="utf-8").read())

    spec = load_spec(str(dest))
    # Should be a dict with a "tests" key
    assert "tests" in spec and isinstance(spec["tests"], list)

    first = spec["tests"][0]
    assert first["name"] == "Greeting includes ‘Hello’"
    assert first["prompt"] == "Hello, World!"
    assert first["checks"]["contains"] == "Hello"


def test_invalid_yaml_raises(tmp_path):
    bad_file = tmp_path / "bad.yml"
    bad_file.write_text("::: not valid YAML :::")
    with pytest.raises(Exception):
        load_spec(str(bad_file))


def test_load_spec_file_not_found():
    with pytest.raises(FileNotFoundError):
        load_spec("no_such_file.yml")


def test_load_spec_empty_file(tmp_path):
    empty = tmp_path / "empty.yml"
    empty.write_text("")
    with pytest.raises(ValueError):
        load_spec(str(empty))


def test_load_spec_list_yaml(tmp_path):
    lst = tmp_path / "list.yml"
    lst.write_text("- a\n- b")
    with pytest.raises(ValueError):
        load_spec(str(lst))


def test_load_spec_missing_tests_key(tmp_path):
    data = tmp_path / "no_tests.yml"
    data.write_text("foo: bar")
    spec = load_spec(str(data))
    assert spec == {"foo": "bar"}
    from promptguard.runner import run_tests

    results = run_tests(spec)
    assert results.passed
    assert results.test_results == []


def test_loader_tests_not_list(tmp_path):
    f = tmp_path / "a.yml"
    f.write_text("tests: foo")
    with pytest.raises(ValueError):
        load_spec(str(f))


def test_loader_test_entry_not_dict(tmp_path):
    f = tmp_path / "a.yml"
    f.write_text("tests:\n  - foo")
    with pytest.raises(ValueError):
        load_spec(str(f))


def test_loader_test_entry_missing_fields(tmp_path):
    f = tmp_path / "a.yml"
    f.write_text("tests:\n  - name: onlyname")
    with pytest.raises(ValueError):
        load_spec(str(f))
