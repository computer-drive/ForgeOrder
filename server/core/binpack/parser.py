from typing import BinaryIO, Any

from .schema import Field, FieldType
from .exceptions import UnsupportedValueTypeError, IOModeError, UnparsedDataError

class BinParser:

    def __init__(self, fields: list[Field]):
        self.fields = fields

        self.fieldsMap = {field.name: field for field in self.fields}


        self.data: dict[str, Any] = {}

    def parse(self, data: bytes):
        '''
        解析字节序列。
        '''
        result = {}

        offset = 0
        for field in self.fields:
            # 计算结束下标
            endLocation = offset + field.fieldType.size

            # 检查数据是否足够
            if endLocation >= len(data):
                # 数据不够，用默认值填充
                value = field.default
            else:
                # 否则，根据偏移量和大小，获取数据并调用FieldType的decode方法
                value = field.fieldType.decode(data[offset:endLocation])

            result[field.name] = value # 存储解析后的值

            offset += field.fieldType.size # 更新偏移量

        self.data = result
        
        return self

    def parseFile(self, f: BinaryIO):
        '''
        从文件中解析数据。
        '''

        if 'b' not in f.mode:
            raise IOModeError()

        data = f.read()

    
        return self.parse(data)
    
    def getBytes(self) -> bytes:
        '''
        将解析后的数据转换为字节序列。
        '''
        if not self.data:
            raise UnparsedDataError()
        
        result: bytes = b''

        for key, value in self.data.items():
            result += self.fieldsMap[key].fieldType.encode(value)

        return result

    def saveFile(self, f: BinaryIO):
        '''
        将解析后的数据保存到文件。
        '''
        f.write(self.getBytes())


    def __getitem__(self, key: str) -> Any:
        '''
        获取指定字段的值。
        '''
        return self.data[key]

    def __setitem__(self, key: str, value: Any):
        '''
        设置指定字段的值。
        注意：只在内存中生效，使用saveFile方法保存到文件。
        '''
        if key not in self.data:
            raise KeyError(key)
        
        if isinstance(value, self.fieldsMap[key].fieldType.pythonType):
            self.data[key] = value
        else:
            raise UnsupportedValueTypeError(self.fieldsMap[key], value)


    def toDict(self) -> dict[str, Any]:
        '''
        将解析后的数据转换为字典。
        '''

        return self.data

    
        
        
