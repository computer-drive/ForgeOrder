
class RequestException(Exception):
    pass

class ArgumentException(RequestException):  
    def __init__(self, args: list[str]):
        super().__init__(f"Arguments {args} are invalid")
        self.args_ = args