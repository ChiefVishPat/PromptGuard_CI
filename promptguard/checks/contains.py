import logging

logger = logging.getLogger(__name__)


def check_contains(output: str, substring: str) -> bool:
    """
    Returns True if `substring` appears anywhere in `output`
    """
    result = substring in output
    logger.debug(f"check_contains: '{substring}' in output => {result}")
    return result
