from dataclasses import dataclass

from .errors import ValidationError
@dataclass
class ValidationResult:
    success: bool
    error: 'ValidationError | None' = None
    # can_fix: bool = True
