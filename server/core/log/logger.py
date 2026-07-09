import datetime
import logging
import queue
import json

from const import *

from .log_db import LogDatabase
from .worker import create_worker


class Logger(logging.Logger):
    def __init__(self, name: str):
        super().__init__(name)

    def log(self, msg: str | dict | list , level: int, class_name: str, method: str): # type:ignore
        extra = {"class_name": class_name, "method": method}

        if isinstance(msg, (dict, list)):
            msg = json.dumps(msg, ensure_ascii=False)
        elif msg is None:
            msg = ''
        else:
            msg = str(msg)

        super().log(level, msg, extra=extra)

    def info(self, msg: str | dict | list , class_name: str, method: str):  # type:ignore
        self.log(msg, logging.INFO, class_name, method)

    def warning(self, msg: str | dict | list , class_name: str, method: str):  # type:ignore
        self.log(msg, logging.WARNING, class_name, method)

    def error(self, msg: str | dict | list , class_name: str, method: str):  # type:ignore
        self.log(msg, logging.ERROR, class_name, method)

    def critical(self, msg: str | dict | list , class_name: str, method: str):  # type:ignore
        self.log(msg, logging.CRITICAL, class_name, method)

    def debug(self, msg: str | dict | list , class_name: str, method: str):  # type:ignore
        self.log(msg, logging.DEBUG, class_name, method)

class DatabaseHandler(logging.Handler):
    def __init__(self, queue: queue.Queue):
        super().__init__()

        self.q = queue

    def emit(self, record: logging.LogRecord):
        
        time = datetime.datetime.fromtimestamp(record.created)

        level = 0

        match record.levelname:
            case "DEBUG":
                level = logging.DEBUG
            case "INFO":
                level = logging.INFO
            case "WARNING":
                level = logging.WARNING
            case "ERROR":
                level = logging.ERROR
            case "CRITICAL":
                level = logging.CRITICAL
            case _:
                level = logging.INFO

        self.q.put((time, level, record.class_name, record.method, record.msg))
        
        

    

class Formatter(logging.Formatter):

    def format(self, record: logging.LogRecord) -> str:
        
        record.color = ""
        record.reset = "\033[0m"

        if record.msg != '':
            record.msg = f": {record.msg}"
        
        match record.levelname:
            case "DEBUG":
                record.levelname = "\033[94mDEBUG\033[0m"
            case "INFO":
                record.levelname = "\033[92mINFO\033[0m"
            case "WARNING":
                record.color = "\033[93m"
            case "ERROR":
                record.color = "\033[91m"
            case "CRITICAL":
                record.color = "\033[95m"

        return super().format(record)



def setup_logger(name: str, db_name: str, level: str = "info"):
    logger = Logger(name)

    formatter = Formatter(LOG.FORMAT)

    level_int = logging.INFO
    match level:
        case "debug":
            level_int = logging.DEBUG
        case "info":
            level_int = logging.INFO
        case "warning":
            level_int = logging.WARNING
        case "error":
            level_int = logging.ERROR
        case "critical":
            level_int = logging.CRITICAL
        case _:
            level_int = logging.INFO
    
    logger.setLevel(level_int)

    # 控制台日志记录器

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    stream_handler.setLevel(level_int)
    logger.addHandler(stream_handler)

    # 数据库日志记录器

    queue, thread = create_worker(db_name)

    db_handler = DatabaseHandler(queue)
    db_handler.setFormatter(formatter)
    db_handler.setLevel(level_int)
    logger.addHandler(db_handler)

    return logger, thread, queue



    

