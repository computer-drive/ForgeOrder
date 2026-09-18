from .base import Serializer

class StringSerializer(Serializer[str]):
    '''
    字符串序列化器，支持字符串的序列化和反序列化。
    '''
    
    typeId = 4
    pythonType = str
    
    def serialize(self, value):
        return value.encode('utf-8')
    
    def deserialize(self, data: bytes):
        return data.decode('utf-8')
