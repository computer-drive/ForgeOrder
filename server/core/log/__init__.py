from threading import Thread
from multiprocessing import Queue
from typing import Literal, cast

from .console import getConsoleLogger 
from .context import getLogContext
# 这两行做导出，不是没用，别删！
from .logger import Logger, setupLogger



logger: Logger | None = None
dbLoggerThread : Thread | None = None 
dbLoggerQueue : Queue | None = None 

_databaseName : str  = ""
_level: Literal["info", "debug", "warning", "error", "critical", "_MISSING"]  = "_MISSING"


def initLogger(
            databaseName: str,
            level: Literal["info", "debug", "warning", "error", "critical"], 
                  ):
    global _loggerName, _databaseName, _level, _formatJson

    _databaseName, _level = databaseName, level

def getLogger():
    global logger, dbLoggerThread, dbLoggerQueue
    global _loggerName, _databaseName, _level, _formatJson

    if _level == "_MISSING" or _databaseName == "":
        raise ValueError("Logger not initialized. Please call initLogger first.")

    if logger is None or dbLoggerThread is None or dbLoggerQueue is None:
        logger, dbLoggerThread, dbLoggerQueue = setupLogger(_databaseName, _level)

    return logger

def getQueue():
    if logger:
        return cast(Queue, dbLoggerQueue)

def shutdownLogger():
    global logger, dbLoggerThread, dbLoggerQueue

    if logger and dbLoggerThread and dbLoggerQueue:

        dbLoggerQueue.put(None)

        dbLoggerThread.join()




        





