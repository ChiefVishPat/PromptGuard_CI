import os

from promptguard.loader import load_spec


def test_load_hello_spec(tmp_path):
    # Copy the example YAML into a temp file
    src = os.path.join(os.path.dirname(__file__), "../examples/hello.yml")
    spec = load_spec(src)

    # We expect a dict with a "tests" list
    assert isinstance(spec, dict)
    assert "tests" in spec and isinstance(spec["tests"], list)

    first = spec["tests"][0]
    assert first["name"] == "hello contains world"
    assert first["prompt"] == "Hello, world!"
    assert first["checks"]["contains"] == "world"
