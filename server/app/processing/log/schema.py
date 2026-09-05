from typing import TypedDict

class LogInfo(TypedDict):
    msg: str
    level: int
    category: str