from dataclasses import dataclass
from typing import Any, Generic, TypeVar

from .exceptions import UnsupportedEncodingError, ValueExceededError

T = TypeVar("T")

ENCODING_MAPS = { # 记录不同编码方式下，一个字符占用的字节数（最大）
    'utf-8': 4,
    'gbk': 2,
    'gb2312': 2,
    'gb18030': 4,
    'ascii': 1,
    'utf-16': 4,
    'utf-32': 4,
}

XOR_KEY = 0xA5


@dataclass
class FieldType(Generic[T]):
    pythonType: type[T]
    size: int    # 占用的字节数（实际上是这个数据最大可存的字节数）

    def encode(self, value: T) -> bytes:
        raise NotImplementedError

    def decode(self, data: bytes) -> T:
        raise NotImplementedError

class String(FieldType[str]):
    pythonType: type[str] = str

    def __init__(self, length: int, encoding: str = "utf-8"):
        # 这里的length指的是字符串长度，而不是字节数
        self.encoding: str = encoding

        if encoding not in ENCODING_MAPS:
            raise UnsupportedEncodingError(encoding)
        
        self.size = length * ENCODING_MAPS[encoding]
        self.length = length

    def encode(self, value: str) -> bytes:
        raw = value.encode(self.encoding)

        # 判断长度是否超过最大长度
        if len(raw) > self.size:
            raise ValueExceededError(self, value, f"{self.size} bytes({self.length} char in {self.encoding})")
        elif len(raw) < self.size:
            # 字符串长度不足最大长度，用空字填充
            raw += b"\x00" * (self.size - len(raw))

        return bytes([b ^ XOR_KEY for b in raw]) # 对字符串进行 XOR 加密后返回

    def decode(self, data: bytes) -> str:
        # 对字符串进行 XOR 解密，移除\x00，再解码
        return bytes([b ^ XOR_KEY for b in data]).strip(b"\x00").decode(self.encoding)

class Integer(FieldType[int]):
    pythonType: type[int] = int

    def __init__(self, bits: int = 32):
        # 这里的bits指的是整数占用的位数，而不是字节数
        self.bits: int = bits

        if bits % 8 != 0:
            # 整数占用的位数必须是8的倍数
            raise ValueError(f"bits must be divisible by 8, but got {bits}")

        # 计算占用的字节数
        self.size = bits // 8

        # 计算最大值
        self.max = 2 ** (bits - 1)- 1



    def encode(self, value: int) -> bytes:
        # 整数不进行加密，直接转换为字节序列
        if not (-self.max <= value <= self.max):
            raise ValueExceededError(self, value, f"{self.max} bytes({self.bits} bits, {-self.max} <= value <= {self.max})")


        return value.to_bytes(self.size, byteorder="big", signed=True) # 注意：全部为有符号整数

    def decode(self, data: bytes) -> int:
        # 整数不进行解密，直接从字节序列转换为整数
        return int.from_bytes(data, byteorder="big", signed=True)

class Boolean(FieldType[bool]):
    pythonType: type[bool] = bool

    def __init__(self):
        self.size = 1

    def encode(self, value: bool) -> bytes:
        # 布尔值转换为字节序列
        return bytes([1 if value else 0])
    
    def decode(self, data: bytes) -> bool:
        # 从字节序列转换为布尔值
        return data[0] == 1

    
@dataclass
class Field(Generic[T]):
    name: str
    fieldType: FieldType[T]
    default: T | None = None
