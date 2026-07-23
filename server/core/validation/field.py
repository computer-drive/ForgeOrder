from dataclasses import dataclass
from typing import Any

from .validators import Validator
from .base import ValidationResult
from .errors import ValueTypeError

@dataclass
class FieldDefinition:
    key: str
    value_type: type
    default: Any
    validator: 'Validator | None' = None

    def verify_value(self, value: Any):
        # print(type(value), self.value_type)
        if isinstance(value, self.value_type):
            if self.validator:
                return self.validator.validate(value)
            else:
                return ValidationResult(True)
        else:
            return ValidationResult(False, ValueTypeError(self.value_type))