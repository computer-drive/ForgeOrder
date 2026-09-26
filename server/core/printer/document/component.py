from typing import Literal
from dataclasses import dataclass

from .reference import Reference
from .reference import ReferenceWithValue as r

class Component:
    pass

@dataclass
class Text(Component):
    text:  Reference[str] = r("")
    font: Reference[Literal["a", "b"]] = r("a")
    align: Reference[Literal["left", "center", "right"]] = r("left")

    underline: Reference[Literal[0, 1, 2]] = r(0) 
    size: Reference[tuple[int, int]] = r((1, 1))
    invert: Reference[bool] = r(False)
    newLine: Reference[bool] = r(True)





 

    
