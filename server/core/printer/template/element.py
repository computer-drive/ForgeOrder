from dataclasses import dataclass
from typing import Literal, Any, cast, TypeVar, Generic

from .reference import Ref, Value

from ..document.component import Component
lazy from ..document.component import  QRCode
lazy from ..document.component import Text as TextComponent

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
    

        
