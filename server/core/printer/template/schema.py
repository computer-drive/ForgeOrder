import unicodedata
from typing import Literal

_LINE_WIDTH = 576 # 每行所占的点阵数

_CHAR_WIDTH = {
    'a': 12,
    'b': 9
}

class Width:
    '''处理点阵宽度与字符宽度之间的问题'''

    def __init__(self, width: int):
        self.width: int = width #单位：点阵

    @staticmethod
    def isChinese(string: str):
        '''判断是否是中文字符'''
        if len(string) != 1:
            raise ValueError("只允许一个字符")

        return unicodedata.east_asian_width(string) in ('F', 'W') 

    @classmethod
    def getStringWidth(cls, string: str, font: Literal['a', 'b'] = 'a', widthScale: int = 1):
        width = 0

        
        for char in string:
            currentWidth = _CHAR_WIDTH[font] * widthScale

            if cls.isChinese(char): 
                currentWidth *= 2

            width += currentWidth

        return Width(width)

    def toCharWidth(self, font: Literal['a', 'b'] = 'a', widthScale: int = 1):
        '''
        将点阵宽度转换为字符宽度。
        注意：中文占两个字符宽度，返回的是等效半角字符的宽度
        '''
        return self.width / _CHAR_WIDTH[font] / widthScale

    def toDotWidth(self):
        return self.width

    


                
LINE_WIDTH = Width(_LINE_WIDTH)