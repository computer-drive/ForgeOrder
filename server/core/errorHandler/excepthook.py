
import sys
import threading
import traceback

from core.log import getConsoleLogger, getLogger
from core.log.formatter import Traceback


def excepthook(type, value, tb, thread: threading.Thread | None = None, ):

    if issubclass(type, KeyboardInterrupt):
        print("用户中止了运行。")

        
    if not thread:
        thread = threading.current_thread()


    

    try:
        logger = getLogger()
    except ValueError:
        consoleLogger = getConsoleLogger("errorHandler")
        consoleLogger.error("".join(traceback.format_exception(type, value, tb)))
        
    else:
        logger.error(
                        {
                        "type": type.__name__,
                        "value": str(value),
                        "traceback": Traceback(traceback.format_exception(type, value, tb)),
                        "thread": thread.name,
                    }, 
                    category="ErrorHandler",
                    action="UncaughtException",
                )
    
            
    
def threadExcepthook(args):
    excepthook(args.exc_type, args.exc_value, args.exc_traceback, args.thread)


def installExcepthook():
    sys.excepthook = excepthook

    threading.excepthook = threadExcepthook