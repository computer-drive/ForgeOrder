from typing import Any, Callable

from .base import Validator
from ..base import ValidationResult
from ..errors import *
from ..exceptions import UnsupportedTypeError, UnsupportedVerifyHandlerError

class NotEmpty(Validator):
    '''
    不可为空。
    允许的类型：str | None
    '''
    allow_types = str | dict | list | None #type: ignore

    def _validate(self, value: Any, context: Any = None):
        is_error = False

        if value is not None :
            if isinstance(value, str):
                if value.strip() == "":
                    is_error = True
            elif isinstance(value, (dict, list)):
                if len(value) == 0:
                    is_error = True

                
        else:
            is_error = True

        if is_error:
            return ValidationResult(False, EmptyError())
        else:
            return ValidationResult(True)


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

class Interval(Validator):
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


        
    def _validate(self, value: Any, context: Any = None):
        if self.min_value.value is not None:
            if self.min_value.inclusive and value >= self.min_value.value:
                pass
            elif not self.min_value.inclusive and value > self.min_value.value:
                pass
            else:
                return ValidationResult(False, IntervalError(self))
            
            
        if self.max_value.value is not None:
            if self.max_value.inclusive and value <= self.max_value.value:
                pass
            elif not self.max_value.inclusive and value < self.max_value.value:
                pass
            else:
                return ValidationResult(False, IntervalError(self))
            
        return ValidationResult(True)
    
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



class Length(Validator):
    '''
    限制值长度在指定范围内。
    允许的类型：str
    '''
    allow_types = str | dict | list | None #type: ignore

    def __init__(self, min_value: int | None, max_value: int | None):
        self.min_value = min_value
        self.max_value = max_value
        
    def _validate(self, value: Any, context: Any = None):
        if not isinstance(value, str):
            return ValidationResult(False, LengthError(self.min_value, self.max_value))

        if self.min_value is not None and len(value) < self.min_value:
            return ValidationResult(False, LengthError(self.min_value, self.max_value))
        if self.max_value is not None and len(value) > self.max_value:
            return ValidationResult(False, LengthError(self.min_value, self.max_value))
        return ValidationResult(True)


class Choices(Validator):
    '''
    限制值只能是指定的选项。
    允许的类型：Any
    '''
    allow_types = None

    def __init__(self, *choices):
        self.choices = choices
        
    def _validate(self, value: Any, context: Any = None):
        if value in self.choices:
            return ValidationResult(True)
        else:
            return ValidationResult(False, ChoicesError(self.choices))


class FunctionHandler(Validator):
    '''
    自定义验证器。
    允许的类型：Any
    '''
    allow_types = None

    def __init__(self, func: Callable):
        self.func = func
        
    def _validate(self, value: Any, context: Any = None):
        result = self.func(value)
        
        if isinstance(result, ValidationResult):
            return result   
        else:
            raise UnsupportedVerifyHandlerError(self.__class__)
