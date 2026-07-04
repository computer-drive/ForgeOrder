from typing import Literal, TypedDict

class UserInfo(TypedDict):
    id: int
    username: str
    password: str
    is_admin: int
    is_available: int
    created_at: str
    last_login_at: str | None

class Token(TypedDict):
    user: UserInfo
    token: str
    expire: int
    device_ip: str
    is_available: bool
    cause_expire: Literal["logout", "expire", "old_device"] | None