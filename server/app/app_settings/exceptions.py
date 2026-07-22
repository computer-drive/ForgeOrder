from app.exceptions import UserError

class SettingsInitError(UserError):
    def __init__(self, msg: str):
        self.msg = msg
        self.hint = "更改数据库表的记录或使用'--fix'参数尝试修复此问题。"
        super().__init__(msg)


class SettingsException(Exception):
    pass


class SettingNotFoundError(SettingsException):
    def __init__(self, key: str):
        self.key = key

        super().__init__(f"Setting '{key}' not found.")

class SettingTypingError(SettingsException):
    def __init__(self, key: str, expected_type: type, value_type: type):
        self.key = key
        self.expected_type = expected_type
        self.value_type = value_type
        
        super().__init__(f"Setting '{key}' expect type {expected_type}, but it is {value_type}.")
        
class SettingVerifyError(SettingsException):
    def __init__(self, key: str, msg: str):
        self.key = key
        self.msg = msg
        
        super().__init__(f"Setting '{key}' verify failed: {msg}")


class TypingConvertError(SettingsException):
    def __init__(self, value, convert_type: type , msg: str = ""):
        self.value = value
        self.convert_type = convert_type
        
        super().__init__(msg)

     