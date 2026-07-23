from typing import Callable, Any

class TypeConvertError(Exception):
    def __init__(self, source_type : type, target_type: type):
        self.source_type = source_type
        self.target_type = target_type

        super().__init__(f"cannot convert type '{source_type}' to '{target_type}'")

class TypeConverterManager:
    def __init__(self):
        self.converters: dict[ tuple[type, type], Callable] = {}
    def register_converter(self, source_type: type, target_type: type, func: Callable):
        self.converters[(source_type, target_type)] = func

    def convert(self, value: Any, target_type: type):
        source_type = type(value)

        if isinstance(value, target_type):
            # 类型一致
            return value

        converter = self.converters.get((source_type, target_type), None)

        if converter:
            return converter(value)
        else:
            raise TypeConvertError(value, target_type)

