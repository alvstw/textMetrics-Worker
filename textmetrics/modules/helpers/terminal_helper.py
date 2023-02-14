from loguru import logger


class TerminalHelper:
    def __init__(self):
        logger.add("logs/textMetrics-{time}.log", format="{time} {level} {message}", level="INFO", rotation="1 day", compression="zip")

    def log(self, message: str):
        logger.info(message)
