
import multiprocessing

from .schema import *

from .database.worker import createWorker



class Logger:
    def __init__(self, level: int, queue: multiprocessing.Queue):
        self.level = level
        self.queue = queue

    def logWithTime(self, message: str | Formatter, data: dict, level: LogLevel, category: str, action: str,  time: datetime.datetime, requestId: str | None = None):
        record = LogRecord(
            time,
            level,
            multiprocessing.current_process().name,
            category,
            action,
            message,
            data,
            requestId
        )

        self.queue.put(record)

    def log(self, message: str | Formatter, data: dict,  level: LogLevel, category: str, action: str, requestId: str | None = None):
        if level.value > self.level:
            return

        record = LogRecord(
            datetime.datetime.now(),
            level,
            multiprocessing.current_process().name,
            category,
            action,
            message,
            data,
            requestId
        )

        self.queue.put(record)

    def info(self, message: str | Formatter, data: dict,  category: str, action: str, requestId: str | None = None):
        self.log(message, data, INFO, category, action, requestId)  

    def debug(self, message: str | Formatter, data: dict,  category: str, action: str, requestId: str | None = None):
        self.log(message, data, DEBUG, category, action, requestId)

    def warning(self, message: str | Formatter, data: dict,  category: str, action: str, requestId: str | None = None):
        self.log(message, data, WARNING, category, action, requestId)

    def error(self, message: str | Formatter, data: dict,  category: str, action: str, requestId: str | None = None):
        self.log(message, data, ERROR, category, action, requestId)

    def notice(self, message: str | Formatter, data: dict,  category: str, action: str, requestId: str | None = None):
        self.log(message, data, NOTICE, category, action, requestId)

    


def setupLogger(databaseName: str, level: str = "info" ):
    level_ = None

    match level:
        case "debug":
            level_ = DEBUG
        case "info":
            level_ = INFO
        case "warning":
            level_ = WARNING
        case "error":
            level_ = ERROR
        case _:
            level_ = INFO

    queue = multiprocessing.Queue()

    thread = createWorker(databaseName, queue)
    
    logger = Logger(level_.value, queue)

    return logger, thread, queue




    

