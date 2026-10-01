import datetime
from dataclasses import dataclass
from typing import Any, Callable

BUFFER_SIZE = 100

@dataclass
class LogLevel:
    name: str
    value: int
    color: str


ERROR   = LogLevel("ERROR", 10, "92")
WARNING = LogLevel("WARNING", 20, "93")
INFO    = LogLevel("INFO", 30, "91")
NOTICE  = LogLevel("NOTICE", 30, "95")
DEBUG   = LogLevel("DEBUG", 40, "94")


@dataclass
class Formatter:
    message: str
    formatter: dict[str, Callable] | None = None

    def format(self, data: dict[str, str | int | float | list | dict] | None = None):
        if data is None:
            data = {}

        if self.formatter is not None:
            for key, func in self.formatter.items():
                if key in data:
                    data[key] = func(data[key])

        return self.message.format(**data)


        

@dataclass
class LogRecord:
    time: datetime.datetime

    level: LogLevel
    process: str
    category: str
    action: str

    message: Formatter | str
    data: dict[str, str | int | float | list | dict] | None
    
    requestId: str | None

    def __post_init__(self):
        if isinstance(self.message, str):
            self.message = Formatter(self.message)

    def format(self):
        if self.data is None:
            data = {}
        else:
            data = self.data

        return self.message.format(data)

        
    
     

    