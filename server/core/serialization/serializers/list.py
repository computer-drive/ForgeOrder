from .base import Serializer

class ListSerializer(Serializer[list]):
    '''
    列表序列化器，支持列表的序列化和反序列化。
    '''
    typeId = 6
    pythonType = list

    def serialize(self, value: list) -> bytes:
        result = b''

        for item in value:
            result += self.manager.serialize(item)

        return result
    
    def deserialize(self, data: bytes) -> list:
        result = []

        while data:
            # 获取类型ID和长度
            typeId = int.from_bytes(data[:2], byteorder='big')
            length = int.from_bytes(data[2:6], byteorder='big')

            # 读取数值，生成新的data
            value = data[6:6 + length]
            data = data[6 + length:]

            # 反序列化数值
            result.append(self.manager.deserializeWithTypeId(value, typeId))

        return result




        