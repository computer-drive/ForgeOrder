
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
        super().__init__()

        self.name = name
