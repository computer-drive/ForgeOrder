from typing import TypeVar, Generic, TYPE_CHECKING


if TYPE_CHECKING:
    from ..manager import SerializationManager

T = TypeVar('T')

class Serializer(Generic[T]):
    typeId: int # 类型ID 1<=typeId<=1024
    pythonType: type # Python类型

    def __init__(self):
        self.manager: 'SerializationManager' = None #type: ignore

    def setManager(self, manager: 'SerializationManager'):
        self.manager = manager

    def serialize(self, value: T) -> bytes:
        raise NotImplementedError

    def deserialize(self, data: bytes) -> T:
        raise NotImplementedError

