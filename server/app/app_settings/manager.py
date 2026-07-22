import json

from .exceptions import *
from app.db.main_db import MainDatabase
# from ...core.config_schema.schema import SettingsProperty, Type
from core.config.validation import SettingsProperty
from .registry import SETTINGS

class SettingsManager:
    def __init__(self, db: MainDatabase):
        self.db = db
        
    def convert(self, value: str, value_type: type):
        '''
        将字符串转换为指定类型。
        '''

        try:
            if value_type == str:
                return value
            elif value_type == int:
                return int(value)
            elif value_type == bool:
                return value == "1" 
            
            elif value_type == list or value_type == dict:
                return json.loads(value)
            else:
                raise TypingConvertError(value, value_type, f"Cannot convert the value to {value_type}.")
        except ValueError as e:
            raise TypingConvertError(value, value_type, f"Failed to convert: {e}")
        
            
    def _init(self):
        for prop in SETTINGS:
            try:
                row = self.db.settings.get(prop.key)
            except TypeError:
                row = None

            if row is None:
                # 不存在则创建
                self.db.settings.insert(prop.key, prop.default)
                continue
            else:
                # 检查值的类型和验证函数
                try:
                    value = self.convert(row["value"], prop.value_type)

                    self._verify(prop.key, value)
                    
                except SettingsException as e:
                    msg = f"设置项'{prop.key}'验证失败："
                    
                    if isinstance(e, SettingNotFoundError):
                        msg += f"设置项是一个无效的项。"
                    elif isinstance(e, SettingTypingError):
                        msg += f"类型错误，应为{e.expected_type}，但实际为{e.value_type}。"

                    elif isinstance(e, SettingVerifyError):
                        msg += f"{e.msg}。"

                    elif isinstance(e, TypingConvertError):
                        msg += f"类型转换错误，{e.value}不能转换为{e.convert_type}。"

                    raise SettingsInitError(msg)

    @staticmethod                    
    def _verify(key, value):
        '''
        更新设置项时验证设置项的有效性。
        
        '''

        property : SettingsProperty | None = next((prop for prop in SETTINGS if prop.key == key), None)
        

        if not property:
            raise SettingNotFoundError(key)
        
        # if not isinstance(value, property.value_type):
        #     raise SettingTypingError(key, property.value_type, type(value))
        
        if property.verify is not None:
            result = property.verify.verify(value)

            if not result.success:
                raise SettingVerifyError(key, str(result.error))
            
        return True




        

        