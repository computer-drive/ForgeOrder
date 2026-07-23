import json
from typing import Any

from .exceptions import *
from app.db.main_db import MainDatabase
from .registry import SETTINGS
from core.type_convert import TypeConverterManager, TypeConvertError



    
con_manager = TypeConverterManager()

con_manager.register_converter(str, int, int)
con_manager.register_converter(int, str, str)

con_manager.register_converter(str, bool, lambda x: x == "1")
con_manager.register_converter(bool, str, lambda x: "1" if x else "0")

con_manager.register_converter(str, list, lambda x: json.loads(x))
con_manager.register_converter(list, str, lambda x: json.dumps(x))

con_manager.register_converter(str, dict, lambda x: json.loads(x))
con_manager.register_converter(dict, str, lambda x: json.dumps(x))



class SettingsManager:
    def __init__(self, db: MainDatabase):
        self.db = db
            
    def _init(self):
        for prop in SETTINGS:

            row = self.db.settings.get(prop.key)

            # print(row)
            if row is None:
                # print(1)
                # 不存在则创建
                self.db.settings.insert(prop.key, prop.default)
                continue
            else:
                try: 
                    value = con_manager.convert(row["value"], prop.value_type)
                except TypeConvertError:
                    raise SettingsInitError(f"类型转换错误，{row["value"]}不能转换为{prop.value_type}。")
                
                try:
        
                    self._verify(prop.key, value)
                    
                except SettingsException as e:
                    msg = f"设置项'{prop.key}'验证失败："
                    
                    if isinstance(e, SettingNotFoundError):
                        msg += f"设置项是一个无效的项。"
                    elif isinstance(e, SettingTypingError):
                        msg += f"类型错误，应为{e.expected_type}，但实际为{e.value_type}。"

                    elif isinstance(e, SettingVerifyError):
                        msg += f"{e.msg}。"

                    raise SettingsInitError(msg)


    def get(self, key: str):
        row = self.db.settings.get(key)

        prop = next((prop for prop in SETTINGS if prop.key == key), None)

        if prop is None:
            raise SettingNotFoundError(key)

        if row is None:
            return prop.default


        return con_manager.convert(row["value"], prop.value_type) # 可能抛出TypeConvertError

    def set(self, key: str, value: Any):
        prop = next((prop for prop in SETTINGS if prop.key == key), None)

        if prop is None:
            raise SettingNotFoundError(key)

        print(prop)
        if not isinstance(value, prop.value_type):
            raise SettingTypingError(key, prop.value_type, type(value))

        value_str = con_manager.convert(value, prop.value_type)


        self.db.settings.update(key, value_str)
        
     
if __name__ == "__main__":

    db = MainDatabase("data/main.db")

    settings_manager = SettingsManager(db)

    settings_manager.set("shop.name", "fuck")

    print(settings_manager.get("shop.name"))






        

        