from concurrent.futures import thread
import datetime
import sys
import threading
import traceback

from core.log.logger import Logger
from .error_report import generate_error_report


def excepthook(type, value, tb, thread: threading.Thread = None):
    import extensions

    if hasattr(extensions, 'logger') and isinstance(extensions.logger, Logger):
        
        if thread:
            extensions.logger.error(
                {
                "type": type.__name__,
                "value": traceback.format_exception(type, value, tb),
                "thread": thread.name,
            }, 
            class_name="ERROR_HANDLER",
            method="ThreadedUncaughtException",
        )
            
        else:
            extensions.logger.error(
            {
                "type": type.__name__,
                "value": traceback.format_exception(type, value, tb),
                # "traceback": str(tb),
            },
            class_name="ERROR_HANDLER",
            method="UncaughtException",
        )
    else:
        print(f"{'Threaded' if thread else ''} Uncaught exception: {type.__name__} in thread '{thread.name if thread else ''}'")
        traceback.print_tb(tb)

    generate_error_report(
        error_type="critical",
        error_title=f"{'Threaded ' if thread else ''}{'Uncaught Exception' if thread else 'Uncaught Exception'}",
        errpr_description=str(value),
        error_detail=traceback.format_exception(type, value, tb),
        time=datetime.datetime.now(),
    )

def thread_excepthook(type, value, tb, thread: threading.Thread):
    excepthook(type, value, tb, thread)

def install():
    sys.excepthook = excepthook

    threading.excepthook = thread_excepthook
