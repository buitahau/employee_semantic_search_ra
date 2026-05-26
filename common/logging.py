import logging

_FMT = '{"time":"%(asctime)s","level":"%(levelname)s","name":"%(name)s","msg":"%(message)s"}'

# Configure root logger once so all loggers (app, uvicorn, etc.) emit output.
logging.basicConfig(level=logging.INFO, format=_FMT)


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
