from dataclasses import dataclass
from typing import Any, Callable

from flask import has_request_context

from .excptions import UnsupportedTypeError, UnsupportedVerifyHandlerError


@dataclass
class SettingsProperty:
    key: str
    value_type: type
    default: Any
    verify: VerifyHandler | None = None

    def verify_value(self, value: Any):
        # print(type(value), self.value_type)
        if isinstance(value, self.value_type):
            if self.verify:
                return self.verify.verify(value)
            else:
                return VerifyResult(True)
        else:
            return VerifyResult(False, ValueTypeError(self.value_type))



class VerifyError:
    
    def __init__(self, msg: str = ""):
        self.msg = msg

    def fix(self, property: SettingsProperty):
        '''
        返回修复好的值
        '''
        return property.default

@dataclass
class VerifyResult:
    success: bool
    error: VerifyError | None = None
    can_fix: bool = True

@dataclass
class ValueTypeError(VerifyError):
    expected_type: type

class VerifyHandler:
    allow_types : type | None = None # None 表示接收任意类型

    def verify(self, value: Any) -> VerifyResult:
        if self.allow_types is None or isinstance(value, self.allow_types):

            result =  self._verify(value)
            can_fix = False
            if hasattr(result.error, 'fix'):
                can_fix = True
            
            return VerifyResult(result.success, result.error, can_fix)
        else:
            # return VerifyResult(False, ValueTypeError(self.allow_types))
        
            raise UnsupportedTypeError(self, self.allow_types, type(value)) #type: ignore
        
    def _verify(self, value: Any) -> VerifyResult: #type: ignore
        pass


class EmptyError(VerifyError):
    
    def fix(self, property: SettingsProperty):
        return property.default

class NotEmpty(VerifyHandler):
    '''
    不可为空。
    允许的类型：str | None
    '''
    allow_types = str | None #type: ignore

    def _verify(self, value: Any):
        if value is not None and isinstance(value, str) and value.strip() != "":
            return VerifyResult(True)
        else:
            return VerifyResult(False, EmptyError())


@dataclass
class IntervalError(VerifyError):
    interval: Interval

    

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


        
    def _verify(self, value: Any):
        if self.min_value.value is not None:
            if self.min_value.inclusive and value >= self.min_value.value:
                pass
            elif not self.min_value.inclusive and value > self.min_value.value:
                pass
            else:
                return VerifyResult(False, IntervalError(self))
            
            
        if self.max_value.value is not None:
            if self.max_value.inclusive and value <= self.max_value.value:
                pass
            elif not self.max_value.inclusive and value < self.max_value.value:
                pass
            else:
                return VerifyResult(False, self)
            
        return VerifyResult(True)
    
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
        
@dataclass
class LengthError(VerifyError):
    min: int | None = None
    max: int | None = None

class Length(VerifyHandler):
    '''
    限制值长度在指定范围内。
    允许的类型：str
    '''
    allow_types = str

    def __init__(self, min_value: int, max_value: int):
        self.min_value = min_value
        self.max_value = max_value
        
    def _verify(self, value: Any):
        if not isinstance(value, str):
            return VerifyResult(False, LengthError(self.min_value, self.max_value))

        if self.min_value <= len(value) <= self.max_value:
            return VerifyResult(True)
        else:
            return  VerifyResult(False, LengthError(self.min_value, self.max_value))

@dataclass
class ChoicesError(VerifyError):
    choices: tuple[Any, ...]

class Choices(VerifyHandler):
    '''
    限制值只能是指定的选项。
    允许的类型：Any
    '''
    allow_types = None

    def __init__(self, *choices):
        self.choices = choices
        
    def _verify(self, value: Any):
        if value in self.choices:
            return VerifyResult(True)
        else:
            return VerifyResult(False, ChoicesError(self.choices))


class FunctionHandler(VerifyHandler):
    '''
    自定义验证器。
    允许的类型：Any
    '''
    allow_types = None

    def __init__(self, func: Callable):
        self.func = func
        
    def _verify(self, value: Any):
        result = self.func(value)
        
        if isinstance(result, VerifyResult):
            return result   
        else:
            raise UnsupportedVerifyHandlerError(self.__class__)



class AnyOfError(VerifyError):  
    children: list[VerifyError]

    def __init__(self, *children):
        self.children = list(children)

class AnyOf(VerifyHandler):
    '''
    限制值必须匹配任意一个验证器。
    允许的类型：Any
    '''
    allow_types = None
    
    def __init__(self, *verify_handlers: VerifyHandler):
        self.verify_handlers = verify_handlers
    
    def _verify(self, value: Any):
        errors = []
        
        for verify_handler in self.verify_handlers:
            result = verify_handler.verify(value)
            if result.success:
                return result
            else:
                errors.append(result.error)
        
        if len(errors) == 1:
            return VerifyResult(False, errors[0])
        else:
            return VerifyResult(False, AnyOfError(*errors))


class AllOfError(VerifyError):
    children: list[VerifyError]

    def __init__(self, *children):
        self.children = list(children)

class AllOf(VerifyHandler):
    '''
    限制值必须匹配所有指定验证器。

    允许的类型：Any
    '''
    allow_types = None
    
    def __init__(self, *verify_handlers):
        self.verify_handlers: tuple[VerifyHandler] = verify_handlers
    
    def _verify(self, value: Any):
        errors = []

        for verify_handler in self.verify_handlers:
            result = verify_handler.verify(value)
            if not result.success:
                errors.append(result.error)
            
        if len(errors) == 0:
            return VerifyResult(True)
        elif len(errors) == 1:
            return VerifyResult(False, errors[0])
        else:
            return VerifyResult(False, AllOfError(*errors))
        

