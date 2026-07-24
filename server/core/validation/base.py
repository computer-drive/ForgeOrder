from dataclasses import dataclass
from typing import Any

from .errors import ValidationError

@dataclass
class ValidationResult:
    success: bool
    error: 'ValidationError | None' = None
    # can_fix: bool = True

    def __bool__(self):
        return self.success

def validate(value: Any, validator: 'Validator') -> ValidationResult:
    return validator.validate(value)
