
class UserError(Exception):
    hint: str = ""
    msg: str = ""