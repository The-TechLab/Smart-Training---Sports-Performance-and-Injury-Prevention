import logging


def setup_logging(level: str = "INFO"):
    """Configure the root logger with a simple format.

    Parameters
    ----------
    level: str
        Logging level name (e.g., "INFO", "DEBUG").
    """
    numeric_level = getattr(logging, level.upper(), logging.INFO)
    logging.basicConfig(
        level=numeric_level,
        format="[%(asctime)s] [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
