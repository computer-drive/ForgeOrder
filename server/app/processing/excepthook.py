import traceback
import multiprocessing
import threading
import sys

from .log.record import WorkerLogger

def processExcepthook(type, value, tb, logger: WorkerLogger):
    logger.error({
        "type": type.__name__,
        "value": str(value),
        "traceback": traceback.format_exception(type, value, tb),
        "thread": threading.current_thread().name,
        "process": multiprocessing.current_process().name,
    }, "ErrorHandler", "UncaughtException")


def installProcessExcepthook(logger: WorkerLogger):
    sys.excepthook = lambda x, y, z: processExcepthook(x, y, z, logger)
