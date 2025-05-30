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
    return data
