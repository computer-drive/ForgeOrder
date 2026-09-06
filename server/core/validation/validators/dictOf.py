from dataclasses import dataclass
from typing import Any
from collections import Counter

from .base import Validator, ValidationResult
from .._errors import ValidationError, ValueTypeError

@dataclass
class _Field:
    key: str
    valueType: type
    required: bool
    validator: Validator | None = None

class FieldTypeError(ValidationError):
    fieldKey: str
    expectedType: type

    def __init__(self, fieldKey: str, expectedType: type):
        self.fieldKey = fieldKey
        self.expectedType = expectedType

    def __str__(self) -> str:
        return f"Field '{self.fieldKey}' must be of type {self.expectedType}."

class MissingRequiredFieldError(ValidationError):
    fieldKey: str

    def __init__(self, fieldKey: str):
        self.fieldKey = fieldKey

    def __str__(self) -> str:
        return f"Missing required field '{self.fieldKey}'."

class FieldValidationError(ValidationError):
    fieldKey: str
    error: ValidationError

    def __init__(self, fieldKey: str, error: ValidationError):
        self.fieldKey = fieldKey
        self.error = error

    def __str__(self) -> str:
        return f"Field '{self.fieldKey}' validation error: {self.error}"

class UndefinedFieldError(ValidationError):
    fieldKey: str

    def __init__(self, fieldKey: str):
        self.fieldKey = fieldKey

    def __str__(self) -> str:
        return f"Field '{self.fieldKey}' is not defined in the schema."


class DictOfError(ValidationError):
    children: list[ValidationError]

    def __init__(self, *children):
        self.children = list(children)

    def __str__(self) -> str:
        return "Dictionary field validation failed:  " + ", ".join([str(child) for child in self.children])



class DictOf(Validator):
    '''
    规定字典的键值对信息。键值对名称、类型、必填项、默认值、验证器。

    非严格模式下，未被定义的键值对将被忽略

    允许的类型：dict
    '''
    allowTypes = None

    def __init__(self, strictMode: bool = False, *fields: _Field):
        self.fields: list[_Field] = list(fields)

        self.strictMode = strictMode

    
    def Field(self, key: str, valueType: type, required: bool, validator: Validator | None = None):
        field = _Field(key, valueType, required, validator)

        self.fields.append(field)

        return self

    def _validate(self, value: dict, context: Any = None):

        errors = []

        fieldKeys = []

        if not isinstance(value, dict):
            return ValidationResult(False, ValueTypeError(dict))

        for field in self.fields:
            key = field.key

            fieldKeys.append(key)

            if key not in value:
                if field.required:
                    errors.append(MissingRequiredFieldError(key))
                    continue

            else:
                if not isinstance(value[key], field.valueType):
                    errors.append(FieldTypeError(key, field.valueType))
                    continue

                if field.validator is not None:
                    result = field.validator.validate(value[key], context)

                    if not result.success:
                        errors.append(FieldValidationError(key, result.error)) #type: ignore

        if self.strictMode:
            for key in value.keys():
                if key not in fieldKeys:
                    errors.append(UndefinedFieldError(key))
            

        if len(errors) == 0:
            return ValidationResult(True)
        else:
            return ValidationResult(False, DictOfError(*errors))

    def mergeAnd(self, other: 'DictOf'):
        return DictOf(self.strictMode & other.strictMode, *(self.fields + other.fields))
    

    def __repr__(self):
        return f"DictOf(strictMode={self.strictMode},\n{"    \n".join([repr(field) for field in self.fields])}\n)"

    def __eq__(self, other): 
        if isinstance(other, DictOf):
            return Counter(self.fields) == Counter(other.fields)
        else:
            return False