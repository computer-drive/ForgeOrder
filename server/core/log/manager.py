from .logger import Logger
import logging

from .exceptions import LoggerIsNotInitializedError


class LogHandler:
    def __init__(self, logger: Logger, class_name: str) -> None:
        self.logger = logger
        self.class_name = class_name

    def log(self, msg: str | dict | list , level: int, method: str):
        self.logger.log(msg, level, self.class_name, method)

    def info(self, msg: str | dict | list , method: str):
        self.log(msg, logging.INFO, method)

    def debug(self, msg: str | dict | list , method: str):
        self.log(msg, logging.DEBUG, method)

    def warning(self, msg: str | dict | list , method: str):
        self.log(msg, logging.WARNING, method)
    
    def error(self, msg: str | dict | list , method: str):
        self.log(msg, logging.ERROR, method)

    def critical(self, msg: str | dict | list , method: str):
        self.log(msg, logging.CRITICAL, method)

def get_log_handler(logger: Logger, class_name: str):

    
    return LogHandler(logger, class_name)

