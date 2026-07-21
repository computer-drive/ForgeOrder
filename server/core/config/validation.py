from dataclasses import dataclass
from typing import Any, Callable, Union

from .excptions import UnsupportedTypeError, UnsupportedVerifyHandlerError


@dataclass
class SettingsProperty:
    key: str
    value_type: type
    default: Any
    verify: VerifyHandler

class VerifyHandler:
    allow_types : type | None = None # None 表示接收任意类型

    def verify(self, value: Any) -> tuple[bool, str]:
        if self.allow_types is None or isinstance(value, self.allow_types):
            return self._verify(value)
        else:
            raise UnsupportedTypeError(self, self.allow_types, type(value)) #type: ignore
        
    def _verify(self, value: Any) -> tuple[bool, str]: #type: ignore
        pass


class NotEmpty(VerifyHandler):
    '''
    不可为空。
    允许的类型：str | None
    '''
    allow_types = str | None #type: ignore

    def _verify(self, value: Any) -> tuple[bool, str]:
        if value is not None and isinstance(value, str) and value.strip() != "":
            return True, ""
        else:
            return False, "value must be not empty."
        
class Range(VerifyHandler):
    '''
    限制值在指定范围内。
    允许的类型：float | int
    '''
    allow_types = float | int #type: ignore

    def __init__(self, min_value: float | int, max_value: float | int):
        self.min_value = min_value
        self.max_value = max_value
        
    def _verify(self, value: Any) -> tuple[bool, str]:
        if not isinstance(value, (float, int)):
            return False, f"value must be float or int type"
        
        if self.min_value <= value <= self.max_value:
            return True, ""
        else:
            return False, f"value must be in {self.min_value} and {self.max_value}"
        
class Length(VerifyHandler):
    '''
    限制值长度在指定范围内。
    允许的类型：str
    '''
    allow_types = str

    def __init__(self, min_value: int, max_value: int):
        self.min_value = min_value
        self.max_value = max_value
        
    def _verify(self, value: Any) -> tuple[bool, str]:
        if not isinstance(value, str):
            return False, f"value must be str type"

        if self.min_value <= len(value) <= self.max_value:
            return True, ""
        else:
            return False, f"value must be in {self.min_value} and {self.max_value}"
        
class Choices(VerifyHandler):
    '''
    限制值只能是指定的选项。
    允许的类型：Any
    '''
    allow_types = None

    def __init__(self, *choices):
        self.choices = choices
        
    def _verify(self, value: Any) -> tuple[bool, str]:
        if value in self.choices:
            return True, ""
        else:
            return False, f"value must be {', '.join(self.choices)}"

class FunctionHandler(VerifyHandler):
    '''
    自定义验证器。
    允许的类型：Any
    '''
    allow_types = None

    def __init__(self, func: Callable):
        self.func = func
        
    def _verify(self, value: Any) -> tuple[bool, str]:
        result = self.func(value)
        
        if isinstance(result, tuple) and len(result) == 2:
            if isinstance(result[0], bool) and isinstance(result[1], str):
                return result
            else:
                raise UnsupportedVerifyHandlerError(self.__class__)
        else:
            raise UnsupportedVerifyHandlerError(self.__class__)
        
class AnyOf(VerifyHandler):
    '''
    限制值必须匹配任意一个验证器。
    允许的类型：Any
    '''
    allow_types = None
    
    def __init__(self, *verify_handlers: VerifyHandler):
        self.verify_handlers = verify_handlers
    
    def _verify(self, value: Any) -> tuple[bool, str]:
        errors = []
        
        for verify_handler in self.verify_handlers:
            result = verify_handler.verify(value)
            if result[0]:
                return result
            else:
                errors.append(result[1])
        
        return False, f"value not pass any of the verify handlers: {', '.join(errors)}"

class AllOf(VerifyHandler):
    '''
    限制值必须匹配所有指定验证器。

    允许的类型：Any
    '''
    allow_types = None
    
    def __init__(self, *verify_handlers):
        self.verify_handlers: tuple[VerifyHandler] = verify_handlers
    
    def _verify(self, value: Any) -> tuple[bool, str]:
        for verify_handler in self.verify_handlers:
            result = verify_handler.verify(value)
            if result[0]:
                return False, result[1]
        else:
            return True, ""
        
   
