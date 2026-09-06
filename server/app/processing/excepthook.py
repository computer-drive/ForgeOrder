import traceback
import multiprocessing
import threading
import sys

from .log.record import WorkerLogger

def _generateErrorMessage(type, value, tb):
    return {
        "type": type.__name__,
        "value": str(value),
        "traceback": traceback.format_exception(type, value, tb),
        "thread": threading.current_thread().name,
        "process": multiprocessing.current_process().name,
    }

def processExcepthook(type, value, tb, logger: WorkerLogger):
    logger.error(_generateErrorMessage(type, value, tb), "ErrorHandler", "UncaughtException")


def installProcessExcepthook(logger: WorkerLogger):
    sys.excepthook = lambda x, y, z: processExcepthook(x, y, z, logger)


    def threadHook(args):
        processExcepthook(
            args.exc_type, 
            args.exc_value, 
            args.exc_traceback, 
            logger
        )
    threading.excepthook = threadHook

