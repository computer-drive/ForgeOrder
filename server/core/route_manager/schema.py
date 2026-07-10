from enum import Enum, auto
from os import name
from typing import TypedDict, Required, NotRequired, Any

class ArgRule(TypedDict):
    name: Required[str]
    type: Required[type]
    required: Required[bool]
    default: NotRequired[Any]




class RouteArgs(TypedDict):
    route: str
    args: list[ArgRule]


class ARGUMENTS:
    class RESULT(Enum):
        PASS = auto()
        FAIL = auto()
        NO_ARGS = auto()

    class ERROR(Enum):
        TYPING_ERROR = auto()
        NOT_FOUND = auto()


