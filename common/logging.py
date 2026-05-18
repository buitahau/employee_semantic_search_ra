import logging


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(
            '{"time":"%(asctime)s","level":"%(levelname)s","name":"%(name)s","msg":"%(message)s"}'
        ))
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger
