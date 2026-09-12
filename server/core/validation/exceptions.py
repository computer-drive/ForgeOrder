from typing import Any
import traceback

lazy from .validators.base import Validator
from ..utils.common import getLanguage

class UnsupportedTypeError(Exception):
    '''
    无法处理这个值的类型。
    '''

    MESSAGES = {
        'en': "Validator ' {} ' does not support type {} , expected type is {}.",
        'zh': "{}验证器不能验证{}类型，但得到了{}类型"
    }
    def __init__(self, validatorClass: type, expectedType: type | tuple[type, ...], valueType: type):
        self.validatorClass = validatorClass
        self.expectedType = expectedType
        self.expectedType = expectedType
        self.valueType = valueType

        super().__init__(
            self.MESSAGES[getLanguage()].format(
                self.validatorClass.__name__,
                self.valueType.__name__,
                self.expectedType.__name__ if isinstance(self.expectedType, type) else ",".join(map(lambda x: x.__name__, self.expectedType))
            )
        )

class NonMergeableValidatorError(Exception):
    '''
    不可合并的验证器
    '''
    MESSAGES = {
        "en": "Validator '{}' is not mergeable.",
        "zh": "{}验证器不可合并"
    }
    

    def __init__(self, validatorClass: type):
        self.validatorClass = validatorClass

        super().__init__(self.MESSAGES[getLanguage()].format(self.validatorClass.__name__))


class UncaughtValidationError(Exception):
    '''
    在验证值时未捕获到的异常。
    '''
    MESSAGES = {
        "en": "An uncaught exception occurred while validating value '{0}' with {1}.\nOriginal Exception: {2}",
        "zh": "{1}验证器在验证值'{0}'时抛出了异常：\n{2}"
    }



    def __init__(self, validator: 'Validator', value: Any, originalException: Exception):
        self.validator = validator
        self.value = value

        if isinstance(originalException, UncaughtValidationError):
            self.originalException = originalException.originalException
        else:
            self.originalException = originalException

        # super().__init__(
        #     f"An uncaught exception occurred while validating value '{self.value}' with {self.validator}\n"
        #     f"Original Exception: {
        #         
        #     }" 
        # )

        super().__init__(self.MESSAGES[getLanguage()].format(
                        self.value,
                        self.validator.__class__.__name__,
                        "\n".join(traceback.format_exception(type(self.originalException),
                        self.originalException,
                        self.originalException.__traceback__))

            ))


