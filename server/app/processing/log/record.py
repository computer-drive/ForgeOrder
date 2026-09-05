from multiprocessing import Queue
import logging
from typing import Callable
import time

lazy from ...utils import g

class WorkerLogger:
    def __init__(self, logQueue: Queue):
        self.logQueue = logQueue

    def log(self, msg: str | dict | list, level: int, category: str, action: str, requestId: str = None): #type: ignore
        self.logQueue.put({
            "timestamp": time.time(),
            "msg": msg,
            "level": level,
            "category": category,
            "action": action,
            "requestId": requestId,
        })

    def debug(self, msg: str | dict | list, category: str, action: str, requestId: str = None): #type: ignore
        self.log(msg, logging.DEBUG, category, action, requestId)

    def info(self, msg: str | dict | list, category: str, action: str, requestId: str = None): #type: ignore
        self.log(msg, logging.INFO, category, action, requestId)

    def warning(self, msg: str | dict | list, category: str, action: str, requestId: str = None): #type: ignore
        self.log(msg, logging.WARNING, category, action, requestId)

    def error(self, msg: str | dict | list, category: str, action: str, requestId: str = None): #type: ignore
        self.log(msg, logging.ERROR, category, action, requestId)

    def critical(self, msg: str | dict | list, category: str, action: str, requestId: str = None): #type: ignore
        self.log(msg, logging.CRITICAL, category, action, requestId)

class WorkerLogContext:
    def __init__(self, logger: WorkerLogger, category: str) -> None:
        self.logger = logger
        self.category = category

    def log(self, msg: str | dict | list , level: int, action: str, requestId: str = None): #type: ignore
        self.logger.log(msg, level, self.category, action, requestId)

    def info(self, msg: str | dict | list , action: str, requestId: str = None): #type: ignore
        self.log(msg, logging.INFO, action, requestId)

    def debug(self, msg: str | dict | list , action: str, requestId: str = None): #type: ignore
        self.log(msg, logging.DEBUG, action, requestId)

    def warning(self, msg: str | dict | list , action: str, requestId: str = None): #type: ignore
        self.log(msg, logging.WARNING, action, requestId)
    
    def error(self, msg: str | dict | list , action: str, requestId: str = None): #type: ignore
        self.log(msg, logging.ERROR, action, requestId)

    def critical(self, msg: str | dict | list , action: str, requestId: str = None): #type: ignore
        self.log(msg, logging.CRITICAL, action, requestId)

class LogContextWithRequestId(WorkerLogContext):
    def __init__(self, logger: WorkerLogger, category: str, requestId: str, onBeforeLog: Callable):
        super().__init__(logger, category)

        self.requestId = requestId
        self.onBeforeLog = onBeforeLog

    def log(self, msg: str | dict | list , level: int, action: str, requestId: str = ""):
        self.onBeforeLog()

        super().log(msg, level, action, self.requestId)

class RequestLogContext(WorkerLogContext):
    def __init__(self, logger: WorkerLogger, category: str = ""):
        super().__init__(logger, category)

            
    def setCategory(self, category: str):
        self.category = category

    def _onBeforeLog(self):
        pass

    def log(self, msg: str | dict | list , level: int, action: str, requestId: str = None): #type: ignore
        self._onBeforeLog()

        return super().log(msg, level, action, g.requestId) 
        
    def getLogContext(self, category: str):
        return LogContextWithRequestId(self.logger, category, g.requestId, self._onBeforeLog)

