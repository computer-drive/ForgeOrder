import traceback
import multiprocessing
import threading
import sys

from core.log import Logger
from core.log.schema import Formatter, ListFormatter
lazy from .base import WorkerPipe


def processExcepthook(type, value, tb, logger: Logger, pipe: 'WorkerPipe'):
    logger.error(Formatter("未捕获的异常：{value} \n {traceback}", {
        "traceback": ListFormatter()
    }), {
        "type": type.__name__,
        "value": str(value),
        "traceback": traceback.format_exception(type, value, tb),
        "thread": threading.current_thread().name,
        "process": multiprocessing.current_process().name,
    }, "ErrorHandler", "UncaughtException")

    pipe.send(
        "uncaughtException",
        {
            "type": type.__name__,
            "value": str(value),
        }
    )


def installProcessExcepthook(logger: Logger, pipe: 'WorkerPipe'):
    sys.excepthook = lambda x, y, z: processExcepthook(x, y, z, logger, pipe)


    def threadHook(args):
        processExcepthook(
            args.exc_type, 
            args.exc_value, 
            args.exc_traceback, 
            logger,
            pipe
        )

    threading.excepthook = threadHook

