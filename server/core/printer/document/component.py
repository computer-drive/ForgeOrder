from typing import Literal
from dataclasses import dataclass

from ...serialization.serializers.custom import ProxySerializer


class Component:
    def print(self) -> None:
        raise NotImplemented

@dataclass
class Text(Component):
    text: str 
    font: Literal["a", "b"] = "a"
    align: Literal["left", "center", "right"] = "left"

    underline: Literal[0, 1, 2] = 0
    size: tuple[int, int] = (1, 1)
    invert: bool = False

    newLine: bool = True

    @property
    def serializer(self):
        return (
            ProxySerializer(201, Text, list,
            lambda x: [x.text, x.font, x.align, x.underline, x.size, x.invert, x.newLine],
            lambda x: Text(text=x[0], font=x[1], align=x[2], underline=x[3], size=x[4], invert=x[5], newLine=x[6])
        ))
        

@dataclass
class QRCode(Component):
    content: str
    size: int = 3 # 二维码大小
    center: bool = False

    @property
    def serializer(self):
        return (
                ProxySerializer(202, QRCode, list,
                lambda x: [x.content, x.size, x.center],
                lambda x: QRCode(content=x[0], size=x[1], center=x[2])
            ))
        

# TODO！
# @dataclass
# class BarCode(Component):
    



        






 

    
