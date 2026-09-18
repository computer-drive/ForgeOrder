from .base import Serializer
from .integer import IntergerSerializer
from .float import FloatSerializer
from .boolean import BooleanSerializer
from .dict import DictSerializer
from .string import StringSerializer
from .list import ListSerializer
from .tuple import TupleSerializer
from .none import NoneSerializer

serializers = [
    IntergerSerializer,
    FloatSerializer,
    BooleanSerializer,
    DictSerializer,
    StringSerializer,
    ListSerializer,
    TupleSerializer,
    NoneSerializer,
]

