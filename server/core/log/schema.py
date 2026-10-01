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


ERROR   = LogLevel("ERROR", 10, "91")
WARNING = LogLevel("WARNING", 20, "93")
INFO    = LogLevel("INFO", 30, "92")
NOTICE  = LogLevel("NOTICE", 30, "95")
DEBUG   = LogLevel("DEBUG", 40, "94")



class ValueFormatter:
    serializer: Serializer 

    def format(self, value: Any) -> str:
        raise NotImplementedError

    def __getstate__(self):
                # 只序列化可pickle的部分
                dct = self.__dict__
                del dct["serializer"]
                return dct
        
    def __setstate__(self, state: dict):

        for k, v in state.items():
            setattr(self, k, v)

        self.serializer = self.getSerializer()

    @classmethod
    def getSerializer(cls) -> Serializer:
        raise NotImplementedError

class ListFormatter(ValueFormatter):

    def __init__(self, char: str = "\n"):
        self.connecter = char

        self.serializer = self.getSerializer()
        
    def format(self, value: list) -> str:
        return self.connecter.join(str(v) for v in value)

    @classmethod
    def getSerializer(cls) -> Serializer:
        return ProxySerializer(
                501, cls, str,
                lambda x: x.connecter,
                lambda x: ListFormatter(x)
            )

class SubItemFormatter(ValueFormatter):

    @classmethod
    def getSerializer(cls):
        return ProxySerializer(
                502, cls, list,
                lambda x: x.keys,
                lambda x: SubItemFormatter(*x)
            )

    def __init__(self, *keys: str):
        self.keys = keys

        self.serializer = self.getSerializer()

    def format(self, value: dict) -> str:
        for key in self.keys:
            if key in value:
                value = value[key]
            else:
                return "<missing: " + key + ">"

        return str(value)

    

def safeFormat(template: str, **kwargs):
    class _D(dict):
        def __missing__(self, key):
            return "{" + key + "}"

    return template.format_map(_D(kwargs))


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
            data_ = {}
        else:
            data_ = data.copy()

        if self.formatter is not None:
            for key, func in self.formatter.items():
                if key in data_:
                    data_[key] = func.format(data_[key])

        return safeFormat(self.message, **data_)

    def __getstate__(self):
        # 只序列化可pickle的部分
        dct = self.__dict__
        del dct["serializer"]
        return dct

    def __setstate__(self, state: dict):
        self.message = state["message"]
        self.formatter = state.get("formatter", None)

        self.serializer = ProxySerializer(
            500, type(self), list,
            lambda x: [x.message, x.formatter],
            lambda x: Formatter(x[0], x[1])
        )

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

        
    
     

    