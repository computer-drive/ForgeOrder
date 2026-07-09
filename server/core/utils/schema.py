from re import S
from typing import TypedDict


class Args(TypedDict):
    arg_name: str
    arg_type: type
    required: bool