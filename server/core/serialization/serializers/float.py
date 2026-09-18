import struct

from .base import Serializer

class FloatSerializer(Serializer[float]):
    '''
    浮点数序列化器，支持32位双精度浮点数的序列化和反序列化。
    '''

    typeId = 3
    pythonType = float

    def serialize(self, value):
        return struct.pack('<d', value)

    def deserialize(self, data: bytes):
        return struct.unpack('<d', data)[0]
    
