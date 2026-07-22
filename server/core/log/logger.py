import datetime
import logging
import queue
import json

from .schema import *

from .log_db import LogDatabase
from .worker import create_worker


class Logger(logging.Logger):
    def __init__(self, name: str):
        super().__init__(name)

        self.ignore_category = []
        self.ignore_action = []
        self.debug_ignore = []

    def setLevel(self, level: int | str) -> None:


        if level == logging.DEBUG:
            import extensions
            self.debug_ignore: list = extensions.config.get("log.debug_ignore")

        return super().setLevel(level)
    
    def setIgnoreCategory(self, category: str) -> None:
        self.ignore_category.append(category)
    
    def setIgnoreAction(self, action: str) -> None:
        self.ignore_action.append(action)


    def log(self, msg: str | dict | list , level: int, category: str, action: str, request_id: str = None): # type:ignore
        extra = {"category": category, "action": action, "request_id": request_id}

        if isinstance(msg, (dict, list)):
            msg = json.dumps(msg, ensure_ascii=False, indent=4)
        elif msg is None:
            msg = ''
        else:
            msg = str(msg)

        if category in self.ignore_category or action in self.ignore_action:
            return
        
        super().log(level, msg, extra=extra)

    def info(self, msg: str | dict | list , category: str, action: str, request_id: str = None):  # type:ignore
        self.log(msg, logging.INFO, category, action, request_id)

    def warning(self, msg: str | dict | list , category: str, action: str, request_id: str = None):  # type:ignore
        self.log(msg, logging.WARNING, category, action, request_id)

    def error(self, msg: str | dict | list , category: str, action: str, request_id: str = None):  # type:ignore
        self.log(msg, logging.ERROR, category, action)

    def critical(self, msg: str | dict | list , category: str, action: str, request_id: str = None):  # type:ignore
        self.log(msg, logging.CRITICAL, category, action, request_id)

    def debug(self, msg: str | dict | list , category: str, action: str, request_id: str = None):  # type:ignore
        # print(category, self.debug_ignore)
        if category in self.debug_ignore:
            return
        else:
            self.log(msg, logging.DEBUG, category, action)

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

        self.q.put((time, level, record.category, record.action, record.msg, record.request_id))
        
        

    

class Formatter(logging.Formatter):

    def format(self, record: logging.LogRecord) -> str:
        
        record.color = ""
        record.reset = "\033[0m"
      
        
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

        if record.request_id:
            record.msg = f": [{record.request_id[:8]}...] {record.msg} "
        else:
            record.msg = f": {record.msg}"

        return super().format(record)



def setup_logger(name: str, db_name: str, level: str = "info"):
    logger = Logger(name)

    formatter = Formatter(FORMAT)

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
    
    if db_name:
        queue, thread = create_worker(db_name)

        db_handler = DatabaseHandler(queue)
        # db_handler.setFormatter(formatter)
        db_handler.setLevel(level_int)
        logger.addHandler(db_handler)
    else:
        queue = None
        thread = None
        logger.warning('', "LOGGER", "NotSetupDatabaseHandler")

    return logger, thread, queue



    

