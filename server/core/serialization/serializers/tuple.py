
from .list import ListSerializer
from .base import Serializer

class TupleSerializer(ListSerializer):
    typeId = 7
    pythonType = tuple

    def serialize(self, value: tuple) -> bytes: #type: ignore
        return super().serialize(list(value))

    def deserialize(self, data: bytes) -> tuple: #type: ignore
        return tuple(super().deserialize(data))

