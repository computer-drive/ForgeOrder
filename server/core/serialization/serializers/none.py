from .base import Serializer

class NoneSerializer(Serializer[None]):
    '''
    None序列化器，支持None类型的序列化和反序列化。
    '''
    
    typeId = 5
    pythonType = type(None)
    
    def serialize(self, value):
        return b''
    
    def deserialize(self, data: bytes):
        return None
