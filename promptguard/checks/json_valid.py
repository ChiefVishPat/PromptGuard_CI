import json
import logging

logger = logging.getLogger(__name__)


def check_json_valid(output: str) -> bool:
    """
    Return True if `output` is valid JSON
    """
    try:
        json.loads(output)
        logger.debug("check_json_valid: output is valid JSON")
        return True
    except json.JSONDecodeError as e:
        logger.debug(f"check_json_valid: invalid JSON ({e})")
        return False
