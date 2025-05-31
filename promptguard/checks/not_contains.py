import logging

logger = logging.getLogger(__name__)


def check_not_contains(output: str, substring: str) -> bool:
    """
    Return True if `subtring` does NOT appear in `output`.
    """
    result = substring not in output
    logger.debug(f"check_not_contains: '{substring}' not in output => {result}")
    return result
