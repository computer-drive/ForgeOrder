
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