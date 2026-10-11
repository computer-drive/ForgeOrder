import multiprocessing
import os
import sys
import threading
import traceback

from ..log import  getLogger
from ..log.schema import Formatter

from .exceptions import CrashException


def terminateChildren(timeout: float = 3):

    children = multiprocessing.active_children()

    for process in children:
        try:
            # 发送 SIGTERM 信号
            process.terminate()
        except Exception as error:
            print(f"终止子进程 {process.name} 失败：{error}")

    for process in children:
        try:
            # 等待子进程退出，若超时则发送 SIGKILL 信号
            process.join(timeout)

            if process.is_alive():
                process.kill()
                process.join(timeout)

        except Exception as error:
            print(f"等待子进程 {process.name} 退出失败：{error}")


def excepthook(type, value, tb, thread: threading.Thread | None = None, ):

    if issubclass(type, KeyboardInterrupt):
        print("用户中止了运行。")

        terminateChildren()

        os._exit(1)

    if issubclass(type, CrashException):
        print("程序已崩溃：")
        print("".join(traceback.format_exception(type, value, tb)))

        sys.stdout.flush()
        sys.stderr.flush()

        terminateChildren()

        # print("bye")

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