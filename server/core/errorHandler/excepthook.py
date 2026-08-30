import datetime
import sys
import threading
import traceback

from core.log.logger import Logger
from .error_report import generateErrorReport
from app.exceptions import UserError
from core.log import getConsoleLogger, getLogger


def generateUserErrorInfo(error: UserError):
    info = f'''程序无法继续运行。原因：
{error.__class__.__name__}: {error.msg}

{error.hint}'''
    logger = getConsoleLogger("errorHandler")
    logger.error(info)

    sys.exit(1)


def excepthook(type, value, tb, thread: threading.Thread | None = None):

    if issubclass(type, UserError):
        generateUserErrorInfo(value)
        return 

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
            category="ERROR_HANDLER",
            action="UncaughtException",
        )
            
    consoleLogger = getConsoleLogger("errorHandler")
    consoleLogger.error(f"Uncaught exception: {type.__name__}: {value}  in thread {thread.name}")
    

    generateErrorReport(
        errorType="critical",
        errorTitle=f"{'Threaded ' if thread else ''}{'Uncaught Exception' if thread else 'Uncaught Exception'}",
        errorDescription=str(value),
        errorDetail=traceback.format_exception(type, value, tb),
        time=datetime.datetime.now(),
    )

def threadExcepthook(args):
    excepthook(args.exc_type, args.exc_value, args.exc_traceback, args.thread)

def install():
    sys.excepthook = excepthook

    threading.excepthook = threadExcepthook