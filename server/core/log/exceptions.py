
class LogException(Exception):
    pass

class LoggerIsNotInitializedError(LogException):
    def __init__(self):
        super().__init__(
            "Logger is not initialized."
        )