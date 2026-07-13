
class EmptyFileException(Exception):
    def __init__(self, file_path: str):
        super().__init__()

        self.file_path = file_path

class CommandNotFoundException(Exception):
    def __init__(self, name: str):
        super().__init__()

        self.name = name


class NotFoundException(Exception):
    def __init__(self, name: str):
        super().__init__(name)

        self.name = name

class ColumnNotFoundException(Exception):
    def __init__(self, table: str,name: str):
        super().__init__(f"Column not found in {table}: {name}")

        self.name = name
        self.table = table