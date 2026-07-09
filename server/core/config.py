import json
import os
from const import CONFIG


class Config:
    def __init__(self, config_file: str):
        self.config_file = config_file
        self.config = None

        self.load()


    def load(self):
        if not os.path.exists(self.config_file):
            with open(self.config_file, 'w', encoding="utf-8") as f:
                json.dump({}, f, indent=4, ensure_ascii=False)
            
            self.config = {}
            return

        with open(self.config_file, "r", encoding="utf-8") as f:
            self.config = json.load(f)

    def save(self):
        with open(self.config_file, "w", encoding="utf-8") as f:
            json.dump(self.config, f, indent=4, ensure_ascii=False)

    def get(self, key: str):
        default = CONFIG.DEFAULT.get(key, None)
        
        if default is None:
            raise ValueError(f"Config key {key} not found in default config")
        
        if self.config is not None:
            return self.config.get(key, default)
        else:
            return default
    
    def set(self, key: str, value):
        if self.config is not None:
            self.config[key] = value
            self.save()
        else:
            raise ValueError("Config file not loaded")
    
    
