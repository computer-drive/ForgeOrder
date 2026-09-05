from dataclasses import dataclass
from typing import Any

from .base import Validator, ValidationResult
from .._errors import ValidationError, ValueTypeError
from ..exceptions import NonMergeableValidatorError


@dataclass
class RangeError(ValidationError):
    _range: 'Range'

    def __str__(self):
        return f"Value must be in {self._range}"

class UncomparableValueError(Exception):

    def __init__(self, valueType: type):

        super().__init__(f"The type of value {valueType} is not compareable.")

class Range(Validator):
    '''
    限制值在一个区间内。
    允许的类型：任何支持>、<、>=、<=运算符的对象
    '''
    allowTypes = None


    def __init__(self):
        
        self.minValue = None
        self.isMinEqual = None
    
        self.maxValue = None
        self.isMaxEqual = None


    def Min(self, value: Any):
        self.minValue = value
        self.isMinEqual = False

        return self

    def Max(self, value: Any):
        self.maxValue = value
        self.isMaxEqual = False

        return self

    def MinEqual(self, value: Any):
        self.minValue = value
        self.isMinEqual = True

        return self

    def MaxEqual(self, value: Any):
        self.maxValue = value
        self.isMaxEqual = True

        return self
        
    def _validate(self, value: Any, context: Any = None):
        if self.minValue is not None:

            try:
                if self.isMinEqual:
                    if value < self.minValue:
                        return ValidationResult(False, RangeError(self))
                else:
                    if value <= self.minValue:
                        return ValidationResult(False, RangeError(self))

            except TypeError:
                raise UncomparableValueError(type(value))

        if self.maxValue:
            try:
                if self.isMaxEqual:
                    if value > self.maxValue:
                        return ValidationResult(False, RangeError(self))
                else:
                    if value >= self.maxValue:
                        return ValidationResult(False, RangeError(self))

            except TypeError:
                raise UncomparableValueError(type(value))
    
    
        return ValidationResult(True)
    
    def __str__(self):
        if self.minValue and self.maxValue:
            return f"{self.minValue} {"<=" if self.isMinEqual else "<"} value {"<=" if self.isMaxEqual else "<"} {self.maxValue}"
        elif self.minValue:
            return f"value {">=" if self.isMinEqual else ">"} {self.minValue}"

        else:
            return f"value {"<=" if self.isMaxEqual else "<"} {self.maxValue}"


    def mergeAnd(self, other: 'Range'):

        newRange = Range()

        # 合并下限

        if self.minValue is None:
            # 没有下限，用other的下限
            newRange.minValue = other.minValue
            newRange.isMinEqual = other.isMinEqual

        elif other.minValue is None:
            # other没有下限，用当前的下限
            newRange.minValue = self.minValue
            newRange.isMinEqual = self.isMinEqual

        else:
            # 均有下限，判断大小

            if self.minValue >= other.minValue:
                newRange.minValue = self.minValue
                newRange.isMinEqual = self.isMinEqual or other.isMinEqual
            
            else:
                newRange.minValue = other.minValue
                newRange.isMinEqual = other.isMinEqual

        # 合并上限
        if self.maxValue is None:
            # 没有上限，用other的上限
            newRange.maxValue = other.maxValue
            newRange.isMaxEqual = other.isMaxEqual
        elif other.maxValue is None:
            # other没有上限，用当前的上限
            newRange.maxValue = self.maxValue
            newRange.isMaxEqual = self.isMaxEqual
        else:
            # 均有上限，判断大小
            if self.maxValue <= other.maxValue:
                newRange.maxValue = self.maxValue
                newRange.isMaxEqual = self.isMaxEqual or other.isMaxEqual
            else:
                newRange.maxValue = other.maxValue
                newRange.isMaxEqual = other.isMaxEqual


        # 检查有效性
        if newRange.minValue is not None and newRange.maxValue is not None:
            if newRange.minValue > newRange.maxValue:
                raise NonMergeableValidatorError(type(newRange))

            if newRange.minValue == newRange.maxValue:
                if not (newRange.isMinEqual and newRange.isMaxEqual):
                    raise NonMergeableValidatorError(type(newRange))

        return newRange

    def __eq__(self, other):
        return (isinstance(other, Range)            and 
                self.minValue   == other.minValue   and
                self.isMinEqual == other.isMinEqual and
                self.maxValue   == other.maxValue   and
                self.isMaxEqual == other.isMaxEqual
                )

    def __repr__(self):
        return f"Range({str(self)})"

                
            


    
    

