import logging

logger = logging.getLogger(__name__)


def check_contains(
    output: str,
    substring: str | list[str],
) -> bool:
    """
    Returns True if `substring` appears anywhere in `output`.
    If a list of substrings is provided, returns True only if all
    substrings are present.
    """
    if isinstance(substring, (list, tuple)):
        # All substrings must be found
        missing = [s for s in substring if s not in output]
        result = not missing
        logger.debug(
            f"check_contains: substrings {substring} in output => {result}, "
            f"missing={missing}"
        )
        return result

    # single substring case
    result = substring in output
    logger.debug(f"check_contains: '{substring}' in output => {result}")
    return result
