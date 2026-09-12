from dataclasses import dataclass
from typing import Literal, Any
import json
import datetime

from .exceptions import *
from core.typeConvert import converter, TypeConvertError

@dataclass
class ColumnType:
    '''列的类型'''
    originType: Literal["INTEGER", "REAL", "TEXT", "BLOB", "NULL"]
    pyType: type | tuple[type, ...]

    
    def validateType(self, value: Any) -> Any:
        '''验证值是否符合类型要求'''
        if value is not None and not isinstance(value, self.pyType):
            # 类型不正确，尝试转换
            try:
                newValue = converter.convert(value, self.pyType)


                return newValue
            except TypeConvertError:
                # 无法转换，抛出异常
                raise TypeMismatchError(self.pyType, type(value)) #type: ignore
        else:
            return value

    def convertTo(self, value: Any) -> Any:
        '''将值转换为数据库可用的类型'''
        if value is None:
            return None
        
        return value

    def convertFrom(self, value: Any) -> Any:
        '''将数据库可用的类型转换为原始类型'''

        if value is None:
            return None
        
        return value

@dataclass
class String(ColumnType):
    '''字符串类型，可指定长度'''
    originType = "TEXT"

    def __init__(self, length: int | None = None):
        self.originType = "TEXT"
        self.length = length

        super().__init__("TEXT", str)

    def convertTo(self, value: str) -> str:
        if value is None:
            return None
        
        if self.length is not None and len(value) > self.length:
            raise StringLengthError(self.length, value)

        return value

    def convertFrom(self, value: str) -> str:
        if value is None:
                    return None
        return value

class Integer(ColumnType):
    '''整数类型'''
    originType = "INTEGER"
    def __init__(self):
        super().__init__("INTEGER", int)

class Real(ColumnType):
    '''浮点数类型'''
    originType = "REAL"

    def __init__(self):
        super().__init__("REAL", float)

class JSON(ColumnType):
    '''JSON类型'''
    originType = "TEXT"

    def __init__(self):
        super().__init__("TEXT", (dict, list))

    def convertTo(self, value: dict | list) -> str:
        if value is None:
                    return None
        
        try:
            return json.dumps(value, ensure_ascii=False)
        except Exception as e:
            raise InvalidJSONError(e)

    def convertFrom(self, value: str) -> dict | list:
        if value is None:
                    return None

        try:
            return json.loads(value)
        except Exception as e:
            raise InvalidJSONError(e)

class DateTime(ColumnType):
    '''日期时间类型'''
    originType = "INTEGER"

    def __init__(self):
        super().__init__("INTEGER", datetime.datetime)

    def convertTo(self, value: datetime.datetime) -> int:
        if value is None:
            return None
        
        return int(value.timestamp() * 1000)

    def convertFrom(self, value: int) -> datetime.datetime:
        if value is None:
            return None

        # 读取数据库并转换为本地时区的时间
        datetime_ =  datetime.datetime.fromtimestamp(value / 1000, tz=datetime.timezone.utc).astimezone() 


        return datetime_.replace(tzinfo=None)



class Boolean(ColumnType):
    '''布尔类型'''
    originType = "INTEGER"

    def __init__(self):
        super().__init__("INTEGER", bool)

    def convertTo(self, value: bool) -> int:
        if value is None:
                    return None
        return int(value)
    
    def convertFrom(self, value: int) -> bool:
        if value is None:
                    return None
        return bool(value)

    








