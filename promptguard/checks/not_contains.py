import logging

logger = logging.getLogger(__name__)


def check_not_contains(
    output: str,
    substring: str | list[str],
) -> bool:
    """
    Return True if `substring` does NOT appear in `output`.
    If a list of substrings is provided, returns True only if none
    of the substrings are present.
    """
    if isinstance(substring, (list, tuple)):
        # None of the substrings may appear
        present = [s for s in substring if s in output]
        result = not present
        logger.debug(
            f"check_not_contains: substrings {substring} not in output => {result}, "
            f"present={present}"
        )
        return result

    # single substring case
    result = substring not in output
    logger.debug(f"check_not_contains: '{substring}' not in output => {result}")
    return result
