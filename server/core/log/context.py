from .logger import Logger
import logging



class WorkerLogContext:
    def __init__(self, logger: Logger, category: str) -> None:
        self.logger = logger
        self.category = category

    def log(self, msg: str | dict | list , level: int, action: str, requestId: str = None):
        self.logger.log(msg, level, self.category, action, requestId)

    def info(self, msg: str | dict | list , action: str, requestId: str = None):
        self.log(msg, logging.INFO, action, requestId)

    def debug(self, msg: str | dict | list , action: str, requestId: str = None):
        self.log(msg, logging.DEBUG, action, requestId)

    def warning(self, msg: str | dict | list , action: str, requestId: str = None):
        self.log(msg, logging.WARNING, action, requestId)
    
    def error(self, msg: str | dict | list , action: str, requestId: str = None):
        self.log(msg, logging.ERROR, action, requestId)

    def critical(self, msg: str | dict | list , action: str, requestId: str = None):
        self.log(msg, logging.CRITICAL, action, requestId)

def getLogContext(logger: Logger, category: str):
    return WorkerLogContext(logger, category)

