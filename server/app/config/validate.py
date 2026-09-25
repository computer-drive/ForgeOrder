# 验证配置项的有效性
import os

from .schema import CONFIG_ITEMS
from core.validation.base import ValidationResult
from core.validation.errors import *
from core.config.jsonConfig import JSONConfig

def validateErrorToStr(error: ValidationResult):
    errorString = ''
    match error:
        case EmptyError():
            errorString = '不能为空'
        case IntervalError():
            errorString = f'数值必须在区间{error.interval}内'
        case LengthError():
            errorString = f"字符串长度必须在{error.min}到{error.max}之间"
        case ChoicesError():
            errorString = f"只能是{','.join(map(str, error.choices))}"
        case AnyOfError():
            childrenErrorString = ''
            for children in error.children:
                childrenErrorString += ' -' + validateErrorToStr(children) + '\n'
            errorString = f'''必须满足以下条件中的一个：
{childrenErrorString}
'''
        case AllOfError():
            childrenErrorString = ''
            for children in error.children:
                childrenErrorString += ' -' + validateErrorToStr(children) + '\n'

            errorString = f'''必须满足以下所有条件：
{childrenErrorString}'''
            
        case ValueTypeError():
            errorString = f'必须是{error.expectedType.__name__}类型'
        
        case _:
            errorString = str(error)

    return errorString

def errorsToString(errors: dict[str, ValidationResult]):
    errorsList = []
    for key, result in errors.items():
        errorsList.append(f"{key}: {validateErrorToStr(result.error)}")

    return errorsList


def validateConfig(config: JSONConfig, fix=False):
    errors: dict[str, ValidationResult] = {}

    for item in CONFIG_ITEMS:
        value = config.get(item.key)

        result = item.validate(value)
                    
        if not result.success:
            errors[item.key] = result
                    
            continue
        else:
            continue


    if errors:
        if fix:
            return errors
        else:
            raise Exception(errorsToString(errors))
    
