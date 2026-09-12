from ...utils.common import getLanguage

class RepositoryError(Exception):
    '''数据库仓库错误'''
    pass

class TypeMismatchError(RepositoryError):
    '''列的类型与值类型不匹配'''

    MESSAGES = {
        'en': 'Expect {}, but got {}',
        'zh': '期望{}类型，但得到了{}类型'
    }
    def __init__(self, expectedType: type, gotType: type):
        super().__init__(
            self.MESSAGES[getLanguage()].format(expectedType, gotType)
        )

class StringLengthError(RepositoryError):
    '''列的类型为String，长度错误'''
    MESSAGES = {
        'en': 'Expect string length <= {}, but got {}',
        'zh': '字符串的长度{}超过了长度限制{}'
    }
    def __init__(self, length: int, value: str):
        super().__init__(
            self.MESSAGES[getLanguage()].format(length, len(value))
        )

class InvalidJSONError(RepositoryError):
    '''列的类型为Json，JSON字符串无效'''
    MESSAGES = {
        'en': 'Invalid JSON: {}',
        'zh': "无效的JSON：{}"
    }
    def __init__(self, originError: Exception):
        self.originError = originError

        super().__init__(
            self.MESSAGES[getLanguage()].format(originError)
        )

class ColumnNotFoundError(RepositoryError):
    '''列名不存在'''
    MESSAGE = {
        'en': 'Column {} not found',
        'zh': '列{}在表中不存在'
    }
    def __init__(self, columnName: str):
        super().__init__(
            self.MESSAGE[getLanguage()].format(columnName)
        )

class EmptyQueryCriteriaError(RepositoryError):
    '''查询参数缺失'''
    MESSAGE = {
        'en': 'Missing query criteria.',
        'zh': '缺失查询参数'
    }

    def __init__(self):
        super().__init__(
            self.MESSAGE[getLanguage()]
        )

class RecordNotFoundError(RepositoryError):
    '''记录不存在'''

    MESSAGES = {
        'en': 'Record not found: {}',
        'zh': '符合查询条件{}的记录不存在'
    }

    def __init__(self, where: dict):
        super().__init__(
            self.MESSAGES[getLanguage()].format(",".join([f"{key}:{value}" for key, value in where.items()]))

        )
