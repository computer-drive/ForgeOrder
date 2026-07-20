from concurrent.futures import thread
import datetime
import sys
import threading
import traceback

from core.log.logger import Logger
from .error_report import generate_error_report
from app.exceptions import UserError

def generate_user_error_info(error: UserError):
    info = f'''程序无法继续运行。原因：
{error.__class__.__name__}: {error.msg}

{error.hint}'''
    print(info)
    sys.exit(1)


def excepthook(type, value, tb, thread: threading.Thread = None):
    import extensions

    if issubclass(type, UserError):
        generate_user_error_info(value)
        return 

    if hasattr(extensions, 'logger') and isinstance(extensions.logger, Logger):
        
        if thread:
            extensions.logger.error(
                {
                "type": type.__name__,
                "value": traceback.format_exception(type, value, tb),
                "thread": thread.name,
            }, 
            category="ERROR_HANDLER",
            action="ThreadedUncaughtException",
        )
            
        else:
            extensions.logger.error(
            {
                "type": type.__name__,
                "value": traceback.format_exception(type, value, tb),
                # "traceback": str(tb),
            },
            category="ERROR_HANDLER",
            action="UncaughtException",
        )
    else:
        print(f"{'Threaded' if thread else ''} Uncaught exception: {type.__name__} in thread '{thread.name if thread else ''}'")
        traceback.print_tb(tb)

    generate_error_report(
        error_type="critical",
        error_title=f"{'Threaded ' if thread else ''}{'Uncaught Exception' if thread else 'Uncaught Exception'}",
        error_description=str(value),
        error_detail=traceback.format_exception(type, value, tb),
        time=datetime.datetime.now(),
    )

def thread_excepthook(args):
    excepthook(args.exc_type, args.exc_value, args.exc_traceback, args.thread)

def install():
    sys.excepthook = excepthook

    threading.excepthook = thread_excepthook