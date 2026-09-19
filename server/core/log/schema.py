import datetime
from dataclasses import dataclass

from .formatter import Formatter

ERROR = 10
WARNING = 20
INFO = 30
DEBUG = 40

BUFFER_SIZE = 100



@dataclass
class LogRecord:
    time: datetime.datetime
    level: int
    category: str
    action: str
    message: dict[str, str | int | float | list | dict | Formatter] | None
    requestId: str | None
    process: str 

    