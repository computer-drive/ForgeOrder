from .base import Serializer

class BooleanSerializer(Serializer[bool]):
    '''
    布尔值序列化器，支持布尔值的序列化和反序列化。
    '''

    typeId = 2
    pythonType = bool

    def serialize(self, value):
        return bytes([1 if value else 0])
    
    def deserialize(self, data: bytes):
        return data[0] == 1