import traceback

from ..utils.common import getLanguage

class SerializerTypeNotFoundError(Exception):
    '''
    序列化器未找到异常。
    '''
    MESSAGES = {
        'en': 'Serializer not found for type {}',
        'zh': '未找到{}类型的序列化器',
    }

    def __init__(self, valueType: type):

        super().__init__(self.MESSAGES[getLanguage()].format(valueType.__name__))

class SerializerIdNotFoundError(Exception):
    '''
    序列化器未找到异常。
    '''
    MESSAGES = {
        'en': 'Serializer not found for id {}',
        'zh': '未找到ID为{}的序列化器',
    }

    def __init__(self, typeId: int):

        super().__init__(self.MESSAGES[getLanguage()].format(typeId))

class SerializationValueOverflowError(Exception):
    '''
    序列化后的数据长度超过2^31异常。
    '''
    MESSAGES = {
        'en': 'Serialized data length exceeds 2^32',
        'zh': '序列化后的数据不能超过2^31字节',
    }

    def __init__(self):
        super().__init__(self.MESSAGES[getLanguage()])


class SerializationError(Exception):
    '''
    序列化错误异常。
    '''
    MESSAGES = {
        'en': 'Serialization error:{} Original Exception {}',
        'zh': '序列化过程中发生错误：{}。原始异常：{}',
    }

    def __init__(self, originException: Exception):
        self.originException = originException

        if isinstance(originException, SerializationError):
            raise originException.originException from None
        
        super().__init__(self.MESSAGES[getLanguage()].format(
            str(originException),
            traceback.format_exc(),
            ))

class DeserializationError(Exception):
    '''
    反序列化错误异常。
    '''
    MESSAGES = {
        'en': 'Deserialization error:{} Original Exception {}',
        'zh': '反序列化过程中发生错误：{}。原始异常：{}',
    }

    def __init__(self, originException: Exception):
        self.originException = originException

        if isinstance(originException, DeserializationError):
            raise originException.originException from None
        
        super().__init__(self.MESSAGES[getLanguage()].format(
            str(originException),
            traceback.format_exc(),
            ))

        
__all__ = [
    'SerializerTypeNotFoundError',
    'SerializerIdNotFoundError',
    'SerializationValueOverflowError',
    'SerializationError',
    'DeserializationError',
]
