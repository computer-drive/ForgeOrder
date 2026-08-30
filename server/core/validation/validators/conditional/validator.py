from typing import Any

from ..base import Validator, ValidationResult
from ..._errors import ValidationError
from .condition import Condition

class If(Validator):
    allowTypes = None
    
    def __init__(self, condition: Condition, validator: Validator):
        self.condition = condition
        self.validator = validator

        self.elseValidator = None
    
    def _validate(self, value: Any, context: Any = None):
        if self.condition.check(context):
            return self._formatResult(self.validator.validate(value, context))
        elif self.elseValidator is not None:
            return self._formatResult(self.elseValidator.validate(value, context))
        else:
            return ValidationResult(True)

    def _formatResult(self, result: ValidationResult):
        if result.success:
            return result
        else:
            return ValidationResult(False, ValidationError(f"When the condition: '{self.condition}' pass, {result.error}"))

    def Elif(self, condition: Condition, validator: Validator):
        self.elseValidator = Elif(condition, validator)

        return self.elseValidator
    def Else(self, validator: Validator):
        self.elseValidator = Else(validator)
        return self.elseValidator

    def __repr__(self):
        return f"{type(self).__name__}({self.condition}, {self.validator})" + (("." + repr(self.elseValidator)) if self.elseValidator is not None else "")
    
class Elif(If):
    pass

class Else(Validator):
    allowTypes = None

    def __init__(self, validator: Validator):
        self.validator = validator

    def _validate(self, value: Any, context: Any = None):
        return self.validator.validate(value, context)

    def __repr__(self):
        return f"Else({self.validator})"
