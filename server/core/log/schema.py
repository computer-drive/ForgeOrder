import datetime
from dataclasses import dataclass
from typing import Any, Callable

from ..serialization.serializers.base import Serializer
from ..serialization.serializers.custom import ProxySerializer

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



class ValueFormatter:
    serializer: Serializer 
    def format(self, value: Any) -> str:
        raise NotImplemented

class ListFormatter(ValueFormatter):

    def __init__(self, char: str = "\n"):
        self.connecter = char

        self.serializer = ProxySerializer(
                501, type(self), str,
                lambda x: x.connecter,
                lambda x: ListFormatter(x)
            )
        
    def format(self, value: list) -> str:
        return self.connecter.join(str(v) for v in value)


@dataclass
class Formatter:
    message: str
    formatter: dict[str, ValueFormatter] | None = None

    def __post_init__(self):
        self.serializer = ProxySerializer(
                    500, type(self), list,
                    lambda x: [x.message, x.formatter],
                    lambda x: Formatter(x[0], x[1])
                )

    def format(self, data: dict[str, str | int | float | list | dict] | None = None):
        if data is None:
            data = {}

        if self.formatter is not None:
            for key, func in self.formatter.items():
                if key in data:
                    data[key] = func.format(data[key])

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

        
    
     

    