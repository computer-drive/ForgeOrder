from dataclasses import dataclass
from typing import Any

from core.validation.field import FieldDefinition
from core.validation.validators import Validator

@dataclass
class RequestField(FieldDefinition):    

    def __init__(self,
                key: str,
                value_type: type,
                required: bool,
                default: Any = None,
                validator: Validator | None = None
                ):
        super().__init__(key, value_type, default, validator)

        self.required : bool = required

        if not required and default is None:
            raise ValueError(f"unrequired field {key} must have a default value.")
        