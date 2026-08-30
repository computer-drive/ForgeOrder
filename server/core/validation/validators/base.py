from dataclasses import dataclass, field

from ..base import ValidationResult
from typing import Any, TYPE_CHECKING
from ..exceptions import NonMergeableValidatorError, UnsupportedTypeError, UncaughtValidationError



@dataclass(init=False, eq=False)
class Validator:
    allowTypes : type | None = field(repr=False) # None 表示接收任意类型

    def validate(self, value: Any = None, context: Any = None) -> ValidationResult:
        if not (self.allowTypes is None or isinstance(value, self.allowTypes)):
            raise UnsupportedTypeError(type(self), self.allowTypes, type(value))

        try:
            result =  self._validate(value, context)
        except Exception as e:
            raise UncaughtValidationError(self, value, e) from None

        
        return ValidationResult(result.success, result.error)

    
    def _validate(self, value: Any, context: Any = None) -> ValidationResult: #type: ignore
        raise NotImplementedError

    def __call__(self, value: Any, context: Any = None) -> ValidationResult:
        return self.validate(value, context)

    def __and__(self, other: 'Validator') -> 'Validator':
        from .logical import AllOf
        return AllOf(self, other)

    def __or__(self, other: 'Validator') -> 'Validator':
        from .logical import AnyOf
        return AnyOf(self, other)

    def __invert__(self) -> 'Validator':
        from .logical import Not
        return Not(self)

    def mergeAnd(self, other) -> Validator:
        raise NonMergeableValidatorError(type(self))


    def mergeOr(self, other) -> Validator:
        raise NonMergeableValidatorError(type(self))

    def bind(self, value: Any) -> 'ValidatorWithValue':
        return ValidatorWithValue(self, value)

class ValidatorWithValue(Validator):

    def __init__(self, validator: Validator, value: Any):
        self.validator = validator
        self.value = value

    def validate(self, value = None, context = None) -> ValidationResult:
        if value is not None:
            raise ValueError("The value must be None when using 'ValidatorWithValue'.")
        
        return self.validator.validate(self.value, context)