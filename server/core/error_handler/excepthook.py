from concurrent.futures import thread
import datetime
import sys
import threading
import traceback

from core.log.logger import Logger
from .error_report import generate_error_report


def excepthook(type, value, tb, is_threading: bool = False):
    import extensions

    if hasattr(extensions, 'logger') and isinstance(extensions.logger, Logger):
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
        print(f"Uncaught exception: {type.__name__}")
        traceback.print_tb(tb)

    generate_error_report(
        error_type="critical",
        error_title=f"{'Threaded ' if is_threading else ''}{'Uncaught Exception' if is_threading else 'Uncaught Exception'}",
        errpr_description=str(value),
        error_detail=traceback.format_exception(type, value, tb),
        time=datetime.datetime.now(),
    )

def install():
    sys.excepthook = excepthook

    threading.excepthook = lambda type, value, tb: excepthook(type, value, tb, is_threading=True)
