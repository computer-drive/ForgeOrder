from .logger import Logger
import logging



class LogContext:
    def __init__(self, logger: Logger, class_name: str) -> None:
        self.logger = logger
        self.class_name = class_name

    def log(self, msg: str | dict | list , level: int, method: str, request_id: str = None):
        self.logger.log(msg, level, self.class_name, method, request_id)

    def info(self, msg: str | dict | list , method: str, request_id: str = None):
        self.log(msg, logging.INFO, method, request_id)

    def debug(self, msg: str | dict | list , method: str, request_id: str = None):
        self.log(msg, logging.DEBUG, method, request_id)

    def warning(self, msg: str | dict | list , method: str, request_id: str = None):
        self.log(msg, logging.WARNING, method, request_id)
    
    def error(self, msg: str | dict | list , method: str, request_id: str = None):
        self.log(msg, logging.ERROR, method, request_id)

    def critical(self, msg: str | dict | list , method: str, request_id: str = None):
        self.log(msg, logging.CRITICAL, method, request_id)

def get_log_context(logger: Logger, class_name: str):

    
    return LogContext(logger, class_name)

