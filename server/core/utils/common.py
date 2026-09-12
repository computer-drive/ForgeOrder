from uuid import UUID
from typing import Literal
import datetime
import os
import locale

currentLanguage = None

def padString(string: str,
               length: int,
               padChar: str = "0",
               position: Literal["left", "right"] = "left") -> str:
    '''
    根据长度补齐字符串
    '''

    if len(string) >= length:
        return string
    
    padLength = length - len(string)

    if position == "left":
        return padChar * padLength + string
    else:
        return string + padChar * padLength

def uuid7ToDatetime(uuid: UUID) -> datetime.datetime:

    # 转换为时间戳
    timestamp = (uuid.int >> 80) & 0xFFFFFFFFFFFF

    # 转换为datetime
    dt = datetime.datetime.fromtimestamp(timestamp / 1000.0 ) # 转换为小数秒

    # 保留毫秒精度
    dt = dt.replace(microsecond=0)

    dt.astimezone() # 使用系统默认时区

    return dt

def datetimeToShortCode(dt: datetime.datetime):

    dayStart = dt.replace(hour=0, minute=0, second=0, microsecond=0)

    # 计算与00:00:00的差值
    diff = dt - dayStart

    # 计算已经过去的秒数
    seconds = diff.total_seconds()

    return int(seconds)

def uuidToShortCode(uuid: UUID):
    dt = uuid7ToDatetime(uuid)

    return datetimeToShortCode(dt)

def getLanguage():
    global currentLanguage

    if not currentLanguage:
        currentLanguage = locale.getlocale()[0]
        if currentLanguage is None:
            currentLanguage = os.environ.get('LANG', 'en_US')

        currentLanguage = currentLanguage.split("_")[0]

    return currentLanguage

        