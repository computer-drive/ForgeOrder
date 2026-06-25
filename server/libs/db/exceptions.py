
class EmptyFileException(Exception):
    def __init__(self, file_path: str):
        super().__init__()

        self.file_path = file_path
