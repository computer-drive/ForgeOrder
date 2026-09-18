from typing import Generic, TypeVar, Callable

from .base import Serializer
from ..exceptions import ProxySerializeTypeError

T = TypeVar('T')


class ProxySerializer(Serializer[T]):
    '''
    代理序列化器。处理一个类型，使用其他序列化器作为代理处理。
    '''
    def __init__(self, typeId: int,
                pythonType: type[T],
                proxyType: type[T],
                serializeMethod: Callable,
                deserializeMethod: Callable):
        '''
        serializeMethod和deserializeMethod函数需要接受value，返回proxyType类型的值。
        deserializeMethod函数需要接收一个proxyType类型的参数
        '''
        super().__init__()
        self.typeId = typeId
        self.pythonType = pythonType
        self.proxyType = proxyType
        self.serializeMethod: Callable = serializeMethod
        self.deserializeMethod: Callable = deserializeMethod

    def serialize(self, value) -> bytes:
        # 先使用序列化方法序列化为代理类型
        result = self.serializeMethod(value)
        
        # 检查序列化结果是否为代理类型
        if not isinstance(result, self.proxyType):
            raise ProxySerializeTypeError(self.pythonType, self.proxyType)

        # 再使用序列化管理器序列化为实际类型
        return self.manager.serialize(result)
    

    def deserialize(self, data: bytes):
        # 先使用反序列化方法反序列化为代理类型
        proxyValue =self.manager.deserialize(data)

        # 再使用序列化管理器反序列化为实际类型
        return self.deserializeMethod(proxyValue)


class CustomSerializer(Serializer[T]):
    '''
    自定义序列化器。
    '''

    def __init__(self, typeId: int, pythonType: type[T], serializeMethod: Callable, deserializeMethod: Callable):
        super().__init__()

        self.typeId = typeId
        self.pythonType = pythonType
        self.serializeMethod: Callable = serializeMethod
        self.deserializeMethod: Callable = deserializeMethod

    def serialize(self, value) -> bytes:
        return self.serializeMethod(value)

    def deserialize(self, data: bytes):
        return self.deserializeMethod(data)

     
        
               


    