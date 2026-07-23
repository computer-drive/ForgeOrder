from typing import TypedDict, Required, NotRequired, Any

from .field import RequestField



class RoutesInfo(TypedDict):
    is_admin: bool
    auth: bool
    args: dict[str, RequestField]





class ARGUMENTS:
    class RESULT:
        PASS = "PASS"
        FAIL = "FAIL"
        NO_ARGS = "NO_ARGS"

    class ERROR:
        TYPING_ERROR = "TYPING_ERROR"
        NOT_FOUND = "NOT_FOUND"


