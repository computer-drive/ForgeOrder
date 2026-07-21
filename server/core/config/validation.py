from dataclasses import dataclass
from typing import Any, Callable, Union

from .excptions import UnsupportedTypeError, UnsupportedVerifyHandlerError


@dataclass
class SettingsProperty:
    key: str
    value_type: type
    default: Any
    verify: VerifyHandler | None = None

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
        


@dataclass(frozen=True)
class Boundary:
    value: float | int | None
    inclusive: bool

    def symbol_left(self):
        return "(" if self.inclusive else "["
    
    def symbol_right(self):
        return ")" if self.inclusive else "]"
       


def Open(value):
    return Boundary(value, False)


def Closed(value):
    return Boundary(value, True)


class Interval(VerifyHandler):
    '''
    限制值在一个区间内。
    允许的类型：float | int
    '''
    allow_types = float | int #type: ignore

    @staticmethod
    def _normalize(value):
        if value is None:
            return Boundary(None, False) 
        if isinstance(value, (int, float)):
            return Boundary(value, True)
        if isinstance(value, Boundary):
            return value
        
        raise UnsupportedTypeError(Interval, float | int, type(value)) #type: ignore
    


    def __init__(self, min_value: Boundary | None | int | float , max_value: Boundary | None | int | float):
        
        self.min_value = self._normalize(min_value)
        self.max_value = self._normalize(max_value)


        
    def _verify(self, value: Any) -> tuple[bool, str]:
        if self.min_value.value is not None:
            if self.min_value.inclusive and value >= self.min_value.value:
                pass
            elif not self.min_value.inclusive and value > self.min_value.value:
                pass
            else:
                return False, f"value must be in {self}"
            
            
        if self.max_value.value is not None:
            if self.max_value.inclusive and value <= self.max_value.value:
                pass
            elif not self.max_value.inclusive and value < self.max_value.value:
                pass
            else:
                return False, f"value must be in {self}"
            
        return True, ""
    
    def __str__(self):
        if self.min_value.value is None:
            min_value = "-∞"
        else:
            min_value = self.min_value.value

        if self.max_value.value is None:
            max_value = "+∞"
        else:
            max_value = self.max_value.value
            
        return f"{self.min_value.symbol_left()}{min_value},{max_value}{self.max_value.symbol_right()}"
        
        
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
            if not result[0]:
                return False, result[1]
        else:
            return True, ""
        
   
