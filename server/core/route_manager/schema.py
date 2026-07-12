# from enum import Enum, auto
# from os import nam/e
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
    class RESULT:
        PASS = "PASS"
        FAIL = "FAIL"
        NO_ARGS = "NO_ARGS"

    class ERROR:
        TYPING_ERROR = "TYPING_ERROR"
        NOT_FOUND = "NOT_FOUND"


