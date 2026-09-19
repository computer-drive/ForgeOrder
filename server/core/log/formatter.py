from dataclasses import dataclass
from typing import Any
import traceback

@dataclass
class Formatter:
    '''
    将一些含有特定含义的消息格式化
    '''
    message: Any

    def format(self):
        raise NotImplementedError

@dataclass
class Traceback(Formatter):
    '''
    格式化Traceback消息
    '''
    message: Exception
    traceback: list[str]

    def format(self):
        print(self.message.__traceback__)
        return "\n".join(self.traceback)


