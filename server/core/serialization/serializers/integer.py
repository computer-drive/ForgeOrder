from .base import Serializer


def integerToBytes(number:int):
    '''
    转换整数为字节数组。无大小限制。有符号。
    '''
    length = 0

    if number >= 0:
        # 整数
        length = (number.bit_length() + 7 + 1) // 8 
        #                                   ^
        #                               这里的 + 1 是留给负号
    else:
        # 负数
        length = ((number + 1).bit_length() + 7 + 1) // 8 
        #                 ^^^
        #                 如果数字是-1的bit_length是0，所以这里要+1
    
    return number.to_bytes(length, byteorder='big', signed=True)

    
class IntegerSerializer(Serializer[int]):
    '''
    整数序列化器，支持32位整符号整数的序列化和反序列化。
    '''
    typeId = 1
    pythonType = int

    def serialize(self, value):
        
        return integerToBytes(value)
    
    def deserialize(self, data: bytes):
        return int.from_bytes(data, byteorder='big', signed=True)


