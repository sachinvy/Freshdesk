import logging


def initialize_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    # create console handler and set level to info
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.debug("Logger Initialized")