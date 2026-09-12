from typing import Any

lazy from .schema import Field
from ..utils.common import getLanguage

class BinpackError(Exception):
    pass

class UnsupportedEncodingError(BinpackError):

    MESSAGES = {
        'en': 'Unsupported encoding: {}',
        'zh': '不支持的编码格式：{}'
    }
    def __init__(self, encoding: str):
        super().__init__(self.MESSAGES[getLanguage()].format(encoding))

class UnsupportedValueTypeError(BinpackError):

    MESSAGES = {
        'en': 'The field {} must be {}, but got {}',
        'zh': '字段{}必须是{}类型，但得到了{}类型'
    }
    def __init__(self, field: 'Field', value: Any):
        super().__init__(self.MESSAGES[getLanguage()].format(field.name, field.fieldType.pythonType.__name__, type(value).__name__))


class IOModeError(BinpackError):

    MESSAGES = {
        'en': 'file must be binary mode.',
        'zh': 'IO对象必须以二进制方式打开'
    }
    def __init__(self):
        super().__init__(self.MESSAGES[getLanguage()])

class UnparsedDataError(BinpackError):

    MESSAGES = {
        'en': 'No data parsed.',
        'zh': '没有解析到数据'
    }
    def __init__(self):
        super().__init__(self.MESSAGES[getLanguage()])

class ValueExceededError(BinpackError):
    MESSAGES = {
        'en': 'The value {} exceeds the maximum {} for the field {}.',
        'zh': '字段{2}的值{0}超过了最大值{1}'
    }
    def __init__(self, field: 'Field', value: Any, msg: str):
        super().__init__(self.MESSAGES[getLanguage()].format(field.name, msg, field.name))

        
