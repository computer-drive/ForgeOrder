# 验证配置项的有效性
import os

import extensions
from .exceptions import ConfigError
from .schema import CONFIG_ITEMS

def verify_config():
    errors = []

    for item in CONFIG_ITEMS:
        value = extensions.config.get(item.key)

        if isinstance(value, item.value_type):
            if item.verify:
                # print(item.key)
                result, msg = item.verify.verify(value)
                
                if result is False:
                    
                    errors.append(f"{item.key}({type(value).__name__}<{value}>)：{msg}")
                
            continue
        else:
            errors.append(f"{item.key}({type(value).__name__}<{value}>)：必须是{item.value_type.__name__}类型")
            

        
    

    if errors:
        raise ConfigError(errors)
