from dataclasses import dataclass
from typing import Any
import traceback

@dataclass
class Formatter:
    '''
    将一些含有特定含义的消息格式化
    '''
    message: Any

    def format(self) -> str:
        raise NotImplementedError

    def formatJSON(self) -> dict | list | str | int | float | None:
        raise NotImplementedError

@dataclass
class Traceback(Formatter):
    '''
    格式化Traceback消息
    '''
    message: Exception
    traceback: list[str]

    def format(self):
        return "\n".join(self.traceback)

    def formatJSON(self):
        return self.traceback


