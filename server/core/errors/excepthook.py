import os
import sys
import threading
import traceback

from ..log import  getLogger
from ..log.schema import Formatter

from .exceptions import CrashException


def excepthook(type, value, tb, thread: threading.Thread | None = None, ):

    if issubclass(type, KeyboardInterrupt):
        print("用户中止了运行。")

        os._exit(1)

    if issubclass(type, CrashException):
        print("程序已崩溃：")
        print("".join(traceback.format_exception(type, value, tb)))

        os._exit(1)

    traceback.print_exception(type, value, tb)
        
        
    if not thread:
        thread = threading.current_thread()

    try:
        logger = getLogger()
    except ValueError:
        print("未捕获的异常：")
        print("".join(traceback.format_exception(type, value, tb)))
        
    else:
        logger.error(
                    Formatter("未捕获的异常（{process} 进程，{thread} 线程）：\n{traceback}"),
                    {
                        "type": type.__name__,
                        "value": str(value),
                        "traceback": "".join(traceback.format_exception(type, value, tb)),
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