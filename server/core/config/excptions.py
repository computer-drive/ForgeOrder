from math import exp


class UnsupportedVerifyHandlerError(Exception):

    '''
    使用FunctionHandler，函数的返回值结构不正确
    '''
    def __init__(self, verify_handler_class: type):
        self.verify_handler_class = verify_handler_class
        
        super().__init__(f"Implemented {verify_handler_class.__name__} in an unsupported way.")
   

class UnsupportedTypeError(Exception):
    '''
    该处理器无法处理这个值的类型。
    '''
    def __init__(self, verify_handler_class: type, expected_type: type, value_type: type):
        self.verify_handler_class = verify_handler_class
        self.expected_type = expected_type
        self.expected_type = expected_type
        self.value_type = value_type

        super().__init__(
            f"Handler '{self.verify_handler_class.__name__}' cannot deal with type {value_type}, expected type is {expected_type}."
        )
