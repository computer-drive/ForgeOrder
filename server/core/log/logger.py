
import multiprocessing

from .schema import *

from .worker import createWorker




class Logger:
    def __init__(self, level: int, queue: multiprocessing.Queue):
        self.level = level
        self.queue = queue

    def logWithTime(self, message: dict | None, level: int, category: str, action: str,  time: datetime.datetime, requestId: str | None = None):
        record = LogRecord(
            time,
            level,
            category,
            action,
            message,
            requestId,
            multiprocessing.current_process().name,
        )

        self.queue.put(record)

    def log(self, message: dict | None, level: int, category: str, action: str, requestId: str | None = None):
        if level > self.level:

            return

        record = LogRecord(
            datetime.datetime.now(),
            level,
            category,
            action,
            message,
            requestId,
            multiprocessing.current_process().name,
        )

        self.queue.put(record)

    def info(self, message: dict | None ,  category: str, action: str, requestId: str | None = None):
        self.log(message, INFO, category, action, requestId)

    def debug(self, message: dict | None ,  category: str, action: str, requestId: str | None = None):
        self.log(message, DEBUG, category, action, requestId)

    def warning(self, message: dict | None ,  category: str, action: str, requestId: str | None = None):
        self.log(message, WARNING, category, action, requestId)

    def error(self, message: dict | None ,  category: str, action: str, requestId: str | None = None):
        self.log(message, ERROR, category, action, requestId)

    


def setupLogger(databaseName: str, level: str = "info" ):
    levelIntger = 0

    match level:
        case "debug":
            levelIntger = DEBUG
        case "info":
            levelIntger = INFO
        case "warning":
            levelIntger = WARNING
        case "error":
            levelIntger = ERROR
        case _:
            levelIntger = INFO

    queue = multiprocessing.Queue()

    thread = createWorker(databaseName, queue)
    
    logger = Logger(levelIntger, queue)

    return logger, thread, queue




    

