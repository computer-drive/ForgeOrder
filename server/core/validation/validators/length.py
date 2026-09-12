from typing import Any
from dataclasses import dataclass
import warnings

from core.validation.exceptions import NonMergeableValidatorError

from .base import Validator, ValidationResult
from .._errors import ValidationError
from ..warnings import ValidationWarning

@dataclass
class LengthError(ValidationError):
    min: int | None = None
    max: int | None = None

    def __str__(self) -> str:
        return f"The length of value must be between {self.min} and {self.max}."

class LengthIsUnavailableError(Exception):
    MESSAGES = {
        "en": "Falied to get the length of {}",
        "zh": "{}类型不能获取长度"

    }
    def __init__(self, valueType: type):
        super().__init__(f"Failed to get the length of {valueType}.")


class Length(Validator):
    '''
    限制值长度在指定范围内。
    允许的类型：str
    '''
    allowTypes = None

    def __init__(self, minValue: int | None, maxValue: int | None):
        self.minValue = minValue
        self.maxValue = maxValue

        if minValue and maxValue and minValue > maxValue:
            warnings.warn("minLength must be less than or equal to maxLength.", category=ValidationWarning)
        
    def _validate(self, value: Any, context: Any = None):

        result = True

        if self.minValue:
            try:
                result = len(value) >= self.minValue
            except ValueError:
                raise LengthIsUnavailableError(type(value))

        if self.maxValue:
            try:
                result = len(value) <= self.maxValue
            except ValueError:
                raise LengthIsUnavailableError(type(value))

        return ValidationResult(
            result,
            None if result else LengthError(self.minValue, self.maxValue)
        )

    def mergeAnd(self, other: 'Length'):

        if self.minValue is None:
            newMin = other.minValue
        elif other.minValue is None:
            newMin = self.minValue
        else:
            newMin = max(self.minValue, other.minValue)

        if self.maxValue is None:
            newMax = other.maxValue
        elif other.maxValue is None:
            newMax = self.maxValue
        else:
            newMax = min(self.maxValue, other.maxValue)

        if newMin is not None and newMax is not None and newMin > newMax:
            raise NonMergeableValidatorError(type(self))

        return Length(newMin, newMax)

    def __eq__(self, other):
        return isinstance(other, Length) and self.minValue == other.minValue and self.maxValue == other.maxValue

                                       
