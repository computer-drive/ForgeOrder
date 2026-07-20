from .logger import Logger
import logging



class LogContext:
    def __init__(self, logger: Logger, category: str) -> None:
        self.logger = logger
        self.category = category

    def log(self, msg: str | dict | list , level: int, action: str, request_id: str = None):
        self.logger.log(msg, level, self.category, action, request_id)

    def info(self, msg: str | dict | list , action: str, request_id: str = None):
        self.log(msg, logging.INFO, action, request_id)

    def debug(self, msg: str | dict | list , action: str, request_id: str = None):
        self.log(msg, logging.DEBUG, action, request_id)

    def warning(self, msg: str | dict | list , action: str, request_id: str = None):
        self.log(msg, logging.WARNING, action, request_id)
    
    def error(self, msg: str | dict | list , action: str, request_id: str = None):
        self.log(msg, logging.ERROR, action, request_id)

    def critical(self, msg: str | dict | list , action: str, request_id: str = None):
        self.log(msg, logging.CRITICAL, action, request_id)

def get_log_context(logger: Logger, category: str):

    
    return LogContext(logger, category)

