from typing import Any
import traceback

lazy from .validators.base import Validator

class UnsupportedTypeError(Exception):
    '''
    无法处理这个值的类型。
    '''
    def __init__(self, validatorClass: type, expectedType: type | tuple[type, ...], valueType: type):
        self.validatorClass = validatorClass
        self.expectedType = expectedType
        self.expectedType = expectedType
        self.valueType = valueType

        super().__init__(
            f"Validator ' {self.validatorClass.__name__}' does not support type {self.valueType}, expected type is {expectedType}."
        )

class NonMergeableValidatorError(Exception):
    '''
    不可合并的验证器
    '''

    def __init__(self, validatorClass: type):
        self.validatorClass = validatorClass

        super().__init__(f"Validator ' {self.validatorClass.__name__}' is not mergeable.")


class UncaughtValidationError(Exception):
    '''
    在验证值时未捕获到的异常。
    '''

    def __init__(self, validator: 'Validator', value: Any, originalException: Exception):
        self.validator = validator
        self.value = value

        if isinstance(originalException, UncaughtValidationError):
            self.originalException = originalException.originalException
        else:
            self.originalException = originalException

        super().__init__(
            f"An uncaught exception occurred while validating value '{self.value}' with {self.validator}\n"
            f"Original Exception: {
                "\n".join(traceback.format_exception(type(self.originalException),
                                                    self.originalException,
                                                    self.originalException.__traceback__))
            }" 
        )


