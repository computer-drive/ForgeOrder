from core.log.logger import Logger
import traceback
from .error_report import generate_error_report
import datetime
import sys

def excepthook(type, value, tb: traceback.TracebackType):
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
        error_title="Uncaught Exception",
        errpr_description=str(value),
        error_detail=traceback.format_exception(type, value, tb),
        time=datetime.datetime.now(),
    )

    sys.exit(1)

def install():
    sys.excepthook = excepthook
