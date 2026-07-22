
import sys
import time

from core.log import get_console_logger


def _fix_config():
    import extensions
    from app.config.schema import CONFIG_ITEMS
    # from core.config.validation import 
    from app.config.verify import verify_config

    logger = get_console_logger("fix")

    errors = verify_config(True)

    if not errors:
        logger.info("未找到配置项问题")
        return

    logger.info(f"找到了{len(errors)}个配置问题")
    

    for key, result in errors.items():
        if not (result.can_fix and result.error is not None):
            logger.warning(f"无法修复配置项{key}")
        else:
            
            property = [item for item in CONFIG_ITEMS if item.key == key][0]

            fixed_value = result.error.fix(property)
            logger.info(f"已修复{key}(默认值：{fixed_value})")


            extensions.config.set(key, fixed_value)
        


def fix(exit: bool = True):
    logger = get_console_logger("fix")
    start_time = time.time()

    
    _fix_config()

    end_time = time.time()

    logger.info(f"修复完成({int(1000 * (end_time - start_time))}ms)")
    

        

