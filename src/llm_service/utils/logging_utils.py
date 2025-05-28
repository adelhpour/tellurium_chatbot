import logging
import sys


def setup_logging(name="llm_service", level=logging.INFO):
    """
    Set up logging with a consistent format

    Args:
        name: Logger name
        level: Logging level

    Returns:
        Configured logger
    """
    logger = logging.getLogger(name)

    if not logger.handlers:
        logger.setLevel(level)

        # Create console handler
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(level)

        # Create formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)

        # Add handler to logger
        logger.addHandler(handler)

    return logger