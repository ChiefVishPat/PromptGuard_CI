from typing import Any, Dict

import yaml


def load_spec(path: str) -> Dict[str, Any]:
    """
    Load a YAML test spec from disk and return it as a Python dict.
    """
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if not isinstance(data, dict):
        raise ValueError(f"Spec at {path} did not parse to a dict")

    # Validate 'tests' structure if present
    tests = data.get("tests", [])
    if "tests" in data and not isinstance(tests, list):
        raise ValueError(f"'tests' section in spec {path} must be a list")
    for idx, test in enumerate(tests, start=1):
        if not isinstance(test, dict):
            raise ValueError(f"Test #{idx} in {path} is not a mapping/dict")
        if "name" not in test or "prompt" not in test:
            raise ValueError(f"Test #{idx} in {path} must include 'name' and 'prompt'")

    return data
