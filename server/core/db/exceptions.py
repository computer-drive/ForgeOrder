class SqlParseException(Exception):
    pass

class EmptyFileError(SqlParseException):
    def __init__(self, file_path: str):
        super().__init__()

        self.file_path = file_path

class CommandNotFoundError(SqlParseException):
    def __init__(self, name: str):
        super().__init__()

        self.name = name


class ExecuteError(Exception):
    def __init__(self, sql: str, origin_error: Exception):
        super().__init__(f"Origin Error: {origin_error} \n SQL: {sql}")

        self.sql = sql
        self.origin_error = origin_error

class NotFoundError(Exception):
    def __init__(self, name: str):
        super().__init__(name)

        self.name = name

class ColumnNotFoundError(Exception):
    def __init__(self, table: str,name: str):
        super().__init__(f"Column not found in {table}: {name}")

        self.name = name
        self.table = table
