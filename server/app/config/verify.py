# 验证配置项的有效性
import os
from ssl import VerifyFlags

from flask.cli import pass_script_info

import extensions
from .exceptions import ConfigError
from .schema import CONFIG_ITEMS
from core.config.validation import *

def verify_error_to_str(error: VerifyError):
    error_str = ''
    match error:
        case EmptyError():
            error_str = '不能为空'
        case IntervalError():
            error_str = f'数值必须在区间{error.interval}内'
        case LengthError():
            error_str = f"字符串长度必须在{error.min}到{error.max}之间"
        case ChoicesError():
            error_str = f"只能是{','.join(map(str, error.choices))}"
        case AnyOfError():
            children_error_str = ''
            for children in error.children:
                children_error_str += ' -' + verify_error_to_str(children) + '\n'
            error_str = f'''必须满足以下条件中的一个：
{children_error_str}
'''
        case AllOfError():
            children_error_str = ''
            for children in error.children:
                children_error_str += ' -' + verify_error_to_str(children) + '\n'

            error_str = f'''必须满足以下所有条件：
{children_error_str}'''
            
        case ValueTypeError():
            error_str = f'必须是{error.expected_type.__name__}类型'
        
        case _:
            error_str = str(error)

    return error_str

def errors_to_str(errors: dict[str, VerifyResult]):
    errors_list = []
    for key, result in errors.items():
        errors_list.append(f"{key}: {verify_error_to_str(result.error)}")

    return errors_list


def verify_config(fix=False):
    errors: dict[str, VerifyResult] = {}

    for item in CONFIG_ITEMS:
        value = extensions.config.get(item.key)

        result = item.verify_value(value)
                    
        if not result.success:
            errors[item.key] = result
                    
            continue
        else:
            continue


    # print(errors)
    if errors:
        if fix:
            return errors
        else:
            raise ConfigError(errors_to_str(errors))
    

    # print("pass")