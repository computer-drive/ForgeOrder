from typing import Any
from dataclasses import dataclass

from .base import Validator, ValidationResult
from .._errors import ValidationError
from .always import AlwaysPass
from .logical import AllOf
from ...utils.common import getLanguage

class NotIterableError(Exception):
    '''
    传入的值不是可迭代对象
    '''

    MESSAGES = {
        "en": "Validator 'ForEach' requires an iterable value, but got {}.",
        "zh": "类型{}时不可迭代的"
    }
    def __init__(self, validatorClass: type, valueType: type):
        self.validatorClass = validatorClass
        self.valueType = valueType

        super().__init__(
            self.MESSAGES[getLanguage()].format(self.valueType)
        )


class ForEachError(ValidationError):
    children: list[ValidationError]

    def __init__(self, *children):
        self.children = list(children)

    def __str__(self) -> str:
        return "Each element of the value must match the following validators: " + ", ".join([str(child) for child in self.children])



class ForEach(Validator):
    '''
    对可迭代对象的每个元素进行验证
    允许的类型：任意可迭代对象
    '''
    allowTypes = None
    
    def __init__(self, *validators: Validator):
        if len(validators) == 0:
            self.validator = AlwaysPass()
        elif len(validators) > 1:
            self.validator = AllOf(*validators)
        else:
            self.validator = validators[0]

    def _validate(self, value: Any, context: Any = None):
        if not hasattr(value, "__iter__"):
            raise NotIterableError(ForEach, type(value))


        errors = []
        for index, item in enumerate(value):
            result = self.validator.validate(item, context)

            if not result.success:
                errors.append(result.error)

        if len(errors) == 0:
            return ValidationResult(True)
        else:
            return ValidationResult(False, ForEachError(*errors))

    def mergeAnd(self, other: 'ForEach'):
        return ForEach(self.validator & other.validator)

    def __eq__(self, other):
        return isintance(other, ForEach) and self.validator == other.validator

