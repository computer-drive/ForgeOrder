
import sys
import threading
import traceback

from core.log import getConsoleLogger, getLogger
from core.log.formatter import Traceback


def excepthook(type, value, tb, thread: threading.Thread | None = None, ):


    if issubclass(type, KeyboardInterrupt):
        logger = getConsoleLogger("errorHandler")
        logger.error("KeyboardInterrupt")
        return 

    
    
    if not thread:
        thread = threading.current_thread()


    logger = getLogger()


    logger.error(
                    {
                    "type": type.__name__,
                    "value": str(value),
                    "traceback": Traceback(value, traceback.format_exception(type, value, tb)),
                    "thread": thread.name,
                }, 
                category="ErrorHandler",
                action="UncaughtException",
            )


            
    consoleLogger = getConsoleLogger("errorHandler")
    consoleLogger.error(f"Uncaught exception: {type.__name__}: {value}  in thread {thread.name}")


def threadExcepthook(args):
    excepthook(args.exc_type, args.exc_value, args.exc_traceback, args.thread)


def installExcepthook():
    sys.excepthook = excepthook

    threading.excepthook = threadExcepthook