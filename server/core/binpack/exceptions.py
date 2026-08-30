from typing import Any

lazy from .schema import Field

class BinpackError(Exception):
    pass

class UnsupportedEncodingError(BinpackError):

    def __init__(self, encoding: str):
        super().__init__(f"Unsupported encoding: {encoding}")

class UnsupportedValueTypeError(BinpackError):
    def __init__(self, field: 'Field', value: Any):
        super().__init__(f"The field {field.name} must be {field.fieldType.pythonType.__name__}, but got {type(value).__name__}.")


class IOModeError(BinpackError):

    def __init__(self):
        return "file must be binary mode."

class UnparsedDataError(BinpackError):
    def __init__(self):
        return "No data parsed."

class ValueExceededError(BinpackError):
    def __init__(self, field: 'Field', value: Any, msg: str):
        super().__init__(f"The value {value} exceeds the maximum {msg} for the field {field.name}.")
