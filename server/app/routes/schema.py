from typing import TypedDict, Required, NotRequired, Any

from .field import RequestField



class RoutesInfo(TypedDict):
    is_admin: bool
    auth: bool
    args: dict[str, RequestField]






