from typing import Any

from .serializers.base import Serializer
from .exceptions import *
from .serializers.integer import integerToBytes
lazy from .serializers import serializers as builtinSerializers

class SerializationManager:
    '''
    序列化管理器，负责注册和管理序列化器。
    '''

    def __init__(self):
        self.serializers: dict[type, type[Serializer]] = {}


    def register(self, serializeClass: type[Serializer]):
        self.serializers[serializeClass.pythonType] = serializeClass

    def getSerializerFromType(self, valueType: type) -> Serializer:
        if valueType in self.serializers:
            return self.serializers[valueType](self)
        else:
            raise SerializerTypeNotFoundError(valueType)

    def getSerializerFromTypeId(self, typeId: int) -> Serializer:
        for serializerClass in self.serializers.values():
            if serializerClass.typeId == typeId:
                return serializerClass(self)
            
        raise SerializerIdNotFoundError(typeId)

    def serialize(self, value: Any) -> bytes:
        try:
            serializer = self.getSerializerFromType(type(value))

            typeId = serializer.typeId.to_bytes(2, byteorder='big') # 转换为2字节大端字节序(1-1024)
            result = serializer.serialize(value)

            if len(result) >= 2**31:
                raise SerializationValueOverflowError()

            length = len(result).to_bytes(4, byteorder='big')


            return typeId + length + result
        except Exception as e:
            raise SerializationError(e) from None

    def deserialize(self, data: bytes) -> Any:
        # 读取前2字节获取typeId
        try:
            typeId = int.from_bytes(data[:2], byteorder='big')

            # 读取4字节获取length
            length = int.from_bytes(data[2:6], byteorder='big')

            # 读取length字节
            result = data[6:6+length]

            return self.getSerializerFromTypeId(typeId).deserialize(result)
        except Exception as e:
            raise DeserializationError(e) from None

    def deserializeWithTypeId(self, data: bytes, typeId: int) -> Any:
        try:
            return self.getSerializerFromTypeId(typeId).deserialize(data)
        except Exception as e:
            raise DeserializationError(e) from None

serializerManager = None

def useSerializerManager():
    global serializerManager

    if serializerManager is None:
        serializerManager = SerializationManager()

        for serializer in builtinSerializers:
            serializerManager.register(serializer)

    return serializerManager

if __name__ == '__main__':
    serializerManager = useSerializerManager()



    data = (serializerManager.serialize({
        "data": "123",
        "fuck": True,
        "data2": 123,
        "data3": 123.456,
        "data12313": None,
        "list": ["123", "123"]
    }))

    print(data)

    print(serializerManager.deserialize(data))


    
