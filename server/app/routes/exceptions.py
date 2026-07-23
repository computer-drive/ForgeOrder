

from core.validation.errors import ValidationError


class RouterManagerException(Exception):
    pass

class RouteAlreadyRegisteredError(RouterManagerException):
    def __init__(self, path: str):
        self.path = path

        super().__init__(f"Route '{self.path}' is Already Registered.")


## 参数验证错误
class ArgumentException(RouterManagerException):
    key: str
    msg: str

class MissingRequiredArgumentError(ArgumentException):
    def __init__(self, key: str):
        self.key = key
        self.msg = f"Argument '{key}' is required."
        super().__init__(self.msg)

class InvalidArgumentTypeError(ArgumentException):
    def __init__(self, key: str, expected_type: type, value_type: type):
        self.key = key
        self.expected_type = expected_type
        self.value_type = value_type
        self.msg = f"Argument '{key}' expected {expected_type.__name__} type, got {value_type.__name__} type."
        super().__init__(self.msg)

class ArgumentValidationError(ArgumentException):
    def __init__(self, key: str, error: ValidationError):
        self.key = key
        self.error = error

        self.msg = f"Argument '{key}' validation error: {error}"
        super().__init__(self.msg)







        

