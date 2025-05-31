import logging
import os

from perspective import PerspectiveAPI

logger = logging.getLogger(__name__)


def check_toxicity(output: str, threshold: float) -> bool:
    """
    Use the Perspective API to score `output` for TOXICITY.
    Return True if the toxicity score is < threshold.
    """
    api_key = os.getenv("PERSPECTIVE_API_KEY", "")
    logger.debug(f"Initializing PerspectiveAPI (key set? {'yes' if api_key else 'no'})")
    client = PerspectiveAPI(api_key=api_key)
    score = client.score(output)["TOXICITY"]
    result = score < threshold
    logger.debug(f"check_toxicity: score={score} threshold={threshold} => {result}")
    return result
