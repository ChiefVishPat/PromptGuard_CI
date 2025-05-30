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
    assert first["name"] == "hello contains world"
    assert first["prompt"] == "Hello, world!"
    assert first["checks"]["contains"] == "world"


def test_invalid_yaml_raises(tmp_path):
    bad_file = tmp_path / "bad.yml"
    bad_file.write_text("::: not valid YAML :::")
    with pytest.raises(Exception):
        load_spec(str(bad_file))
