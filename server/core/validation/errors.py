from dataclasses import dataclass
from typing import Any


class ValidationError:
    msg : str 

    def __init__(self, msg: str = ""):
        self.msg = msg

    def fix(self, property):
        '''
        返回修复好的值
        '''
        return property.default

    def __str__(self) -> str:
        return self.msg



@dataclass
class ValueTypeError(ValidationError):
    expected_type: type

    def __str__(self) -> str:
        return f"The handler only allows {self.expected_type} type."




class EmptyError(ValidationError):
    def __str__(self):
        return "The value cannot be empty."

@dataclass
class IntervalError(ValidationError):
    interval: Any

    def __str__(self):
        return f"Value must be in {self.interval}"

    

    
@dataclass
class LengthError(ValidationError):
    min: int | None = None
    max: int | None = None

    def __str__(self) -> str:
        return f"The length of value must be between {self.min} and {self.max}."


@dataclass
class ChoicesError(ValidationError):
    choices: tuple[Any, ...]

    def __str__(self) -> str:
        return f"The value must be in {self.choices}"




class AnyOfError(ValidationError):  
    children: list[ValidationError]

    def __init__(self, *children):
        self.children = list(children)

    def __str__(self) -> str:
        return "The value must match any of the following validators: " + ", ".join([str(child) for child in self.children])



class AllOfError(ValidationError):
    children: list[ValidationError]

    def __init__(self, *children):
        self.children = list(children)

    def __str__(self) -> str:
        return "The value must match all of the following validators: " + ", ".join([str(child) for child in self.children])
