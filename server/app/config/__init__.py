from typing import Any

from .validate import validateConfig
from core.config.jsonConfig import JSONConfig
from .base import setupConfig
from .schema import CONFIG

class ConfigManager:
    '''全局单例的配置管理器'''
    _config: JSONConfig | None = None
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)   

        return cls._instance

    def initConfig(self, configPath: str):
        '''
        加载配置。在调用`get`和`set`前需调用否则抛出异常。
        '''
        if self._config is None:
            self._config = setupConfig(configPath)

            validateConfig(self._config)

        else:
            raise ValueError("Config is already initialized.")

    

    def get(self, key: str):
        if self._config is None:
            raise ValueError("Config is not initialized.")
        return self._config.get(key)

    def set(self, key: str, value: Any):
        if self._config is None:
            raise ValueError("Config is not initialized.")
        return self._config.set(key, value)

    def getConfigInstance(self):
        if self._config is None:
            raise ValueError("Config is not initialized.")
        
        return self._config

config = ConfigManager()

        