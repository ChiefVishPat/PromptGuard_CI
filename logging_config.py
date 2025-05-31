import logging
import sys


def setup_logging(
    level: int = logging.INFO,
    fmt: str = "%(asctime)s %(levelname)-8s [%(name)s] %(message)s",
    datefmt: str = "%Y-%m-%d %H:%M:%S",
) -> None:
    """
    Configure the root logger to output to stdout with a consistent format.
    """
    root = logging.getLogger()
    root.setLevel(level)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)
    handler.setFormatter(logging.Formatter(fmt=fmt, datefmt=datefmt))

    # Replace any existing handlers
    root.handlers.clear()
    root.addHandler(handler)
