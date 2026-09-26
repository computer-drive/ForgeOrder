from dataclasses import dataclass
from typing import Literal, Any, cast, TypeVar, Generic

from .reference import Ref, Value

from ..document.component import Component
lazy from ..document.component import  QRCode as QRCodeComponent
lazy from ..document.component import Text as TextComponent

from .schema import Width, LINE_WIDTH

T = TypeVar("T")

def _resolve(x: T | Ref[T], context: dict) -> T:
    if isinstance(x, Ref):
        return cast(T, x.render(context))
    
    return x
       

class Element:

    def render(self, context: dict) -> Component:
        raise NotImplemented

    def __post_init__(self):
        # 将所有非引用类型转换为 Value 类型
        for ref, data in self.__dict__.items():
            if not isinstance(data, Ref):
                setattr(self, ref, Value(data))

            setattr(self, ref, cast(Ref[Any], getattr(self, ref)))

@dataclass
class Text(Element):
    text: str | Ref[str]
    font: Literal["a", "b"] | Ref[Literal["a", "b"]] = "a"
    align: Literal["left", "center", "right"] | Ref[Literal["left", "center", "right"]] = "left"

    underline: Literal[0, 1, 2] | Ref[Literal[0, 1, 2]] = 0
    size: tuple[int, int] | Ref[tuple[int, int]] = (1, 1)
    invert: bool | Ref[bool] = False

    newLine: bool | Ref[bool] = True

    def render(self, context: dict):
        return TextComponent(
            _resolve(self.text, context),
            _resolve(self.font, context), 
            _resolve(self.align, context), 
            _resolve(self.underline, context), 
            _resolve(self.size, context),   
            _resolve(self.invert, context),     
            _resolve(self.newLine, context),     
            )

@dataclass
class QRCode(Element):
    content: str | Ref[str]
    size: int | Ref[int]
    center: bool | Ref[bool]

    def render(self, context: dict):
        return QRCodeComponent(
            _resolve(self.content, context),
            _resolve(self.size, context),
            _resolve(self.center, context)
        )

@dataclass
class Divider(Element):
    font: Literal['a', 'b'] | Ref[Literal['a', 'b']] = 'a'
    scale: tuple[int, int] | Ref[tuple[int, int]] = (1, 1)
    char: str | Ref[str] = '-'

    def render(self, context: dict):
        font = _resolve(self.font, context)
        scale = _resolve(self.scale, context)
        char = _resolve(self.char, context)

        return TextComponent(
            char * int(LINE_WIDTH.toCharWidth(font, scale[0])),
            font,
            size=scale
        )
@dataclass
class Column:
    content: str | Ref[str]

    width: int | Ref[int] | None = None
    maxWidth: int | Ref[int] | None = None
    minWidth: int | Ref[int] | None = None
    

@dataclass
class Table(Element):
    columns: list[Column]

    data: list[list[str]] | Ref[list[list[str]]]
    



    

        
