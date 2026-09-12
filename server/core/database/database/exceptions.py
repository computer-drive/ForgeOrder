import sqlite3
from ...utils.common import getLanguage

class DatabaseError(Exception):
    '''数据库连接基类'''
    originError: Exception = None #type: ignore

    def __init__(self, msg: str, originError: Exception = None): #type: ignore
        self.originError = originError

        super().__init__(msg)


class NotConnectedError(DatabaseError):
    '''数据库未连接异常'''

    MESSAGES = {
        'en': 'Database not connected or closed.',
        'zh': '数据库尚未连接或连接已关闭'
    }

    def __init__(self):
        super().__init__(self.MESSAGES[getLanguage()].format())


class DatabaseLockedError(DatabaseError):
    '''数据库锁定异常'''

    MESSAGES = {
        'en': 'Database is locked.',
        'zh': "数据库已被锁定"
    }

    def __init__(self, originError: Exception):
        self.originError = originError

        super().__init__(self.MESSAGES[getLanguage()].format())

class ConstraintError(DatabaseError):
    '''约束错误基类'''  

class UniqueConstraintError(ConstraintError):
    '''唯一(UNIQUE)约束错误'''

    MESSAGES = {
        'en': 'Unique constraint error: {}',
        'zh': '唯一（UNIQUE）约束错误：{}'
    }

    def __init__(self, originError: Exception):
        self.originError = originError

        super().__init__(self.MESSAGES[getLanguage()].format())

class ForeignKeyConstraintError(ConstraintError):
    '''外键约束错误'''

    MESSAGE = {
        'en': 'Foreign key constraint error:{}',
        'zh': '外键（FOREIGN）约束错误:{}'
    }

    def __init__(self, originError: Exception):
        self.originError = originError

        super().__init__(self.MESSAGE[getLanguage()].format(originError))

class PrimaryKeyConstraintError(ConstraintError):
    '''主键约束错误'''

    MESSAGES = {
        'en': 'Primary key constraint error:{}',
        'zh': '主键（PRIMARY）约束错误:{}'
    }
    def __init__(self, originError: Exception):
        self.originError = originError

        super().__init__(self.MESSAGES[getLanguage()].format(originError))
        
class NotNullConstraintError(ConstraintError):
    '''非空约束错误'''

    MESSAGES = {
        'en': 'Not null constraint error:{}',
        'zh': '非空（NOT NULL）约束错误：{}'
    }

    def __init__(self, originError: Exception):
        self.originError = originError

        super().__init__(self.MESSAGES[getLanguage()].format(originError))

class CheckConstraintError(ConstraintError):
    '''检查约束错误'''

    MESSAGES = {
        'en': 'Check constraint error:{}',
        'zh': '检查（CHECK）约束错误：{}'
    }

    def __init__(self, originError: Exception):
        self.originError = originError

        super().__init__(self.MESSAGES[getLanguage()].format(originError))

class DatabaseCannotOpenError(DatabaseError):
    '''数据库无法打开错误'''

    def __init__(self, msg: str, originError: Exception = None): #type: ignore
        self.originError = originError

        super().__init__(msg, originError)


class DatabaseTypeError(DatabaseError):

    MESSAGES = {
        'en': 'Type mismatch. {}',
        'zh': '类型不匹配：{}'
    }

    def __init__(self, originError: Exception):
        self.originError = originError

        super().__init__(self.MESSAGES[getLanguage()].format(originError))

MESSAGES = {
    "unknown": {
        'en': "Unknown databse error: {}",
        "zh": "未知数据库错误：{}"
    },
    "cannotOpen": {
        'en': "Cannot open the databse: {}",
        "zh": "无法打开数据库：{}"
    }
}

def getBasicCode(code: int):
    '''获取SQLite错误码的基本码'''
    return code & 0xff

def convertError(error: sqlite3.Error):
    '''转换数据库错误'''

    sqliteErrorcode = getattr(error, "sqlite_errorcode", None)
    sqliteErrorname = getattr(error, "sqlite_errorname", None)

    if sqliteErrorcode is None:
        return  DatabaseError(MESSAGES["unknown"][getLanguage()].format(error), error)

    match sqliteErrorcode:
        case 5:
            return DatabaseLockedError(error)
        case 2067:
            return UniqueConstraintError(error)
        case 1555:
            return PrimaryKeyConstraintError(error)
        case 787:
            return ForeignKeyConstraintError(error)
        case 1299:
            return NotNullConstraintError(error)
        case 279:
            return CheckConstraintError(error)
        # case 14:
        #     raise DatabaseFileError("Cannot open database file. ", error)
        # case 26:
        #     raise DatabaseFileError("File is not a database.", error)
        # case 13:
        #     raise DatabaseFileError("Disk is full.", error)

        case 20:
            return DatabaseTypeError(error)
        
        case _:
            basicCode = getBasicCode(sqliteErrorcode)

            match basicCode:
                case 14:
                    return DatabaseCannotOpenError(f"({sqliteErrorcode} {sqliteErrorname}) {MESSAGES["cannotOpen"][getLanguage()].format(error)}", error)
                case _:
                    return DatabaseError(f"({basicCode} {sqliteErrorcode} {sqliteErrorname}) {MESSAGES['unknown'][getLanguage()].format(error)}", error)

        
