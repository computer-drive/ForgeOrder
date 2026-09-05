
import sys
import threading
import traceback

from core.log import getConsoleLogger, getLogger


def excepthook(type, value, tb, thread: threading.Thread | None = None, ):


    if issubclass(type, KeyboardInterrupt):
        logger = getConsoleLogger("errorHandler")
        logger.error("KeyboardInterrupt")
        return 

    
    
    if not thread:
        thread = threading.current_thread()

    isLoggerInitialized = True
    try:
        logger = getLogger()
    except ValueError:
        # 日志还未初始化
        isLoggerInitialized = False

    if isLoggerInitialized:
        logger.error(
                {
                "type": type.__name__,
                "value": str(value),
                "traceback": traceback.format_exception(type, value, tb),
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