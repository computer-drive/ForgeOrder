import traceback

from core.utils.common import getLanguage


class PluginInitError(Exception):
    MESSAGES = {
        "zh": "插件{}初始化时出错，原始异常：{}",
        "en": "Pluglin {} init error, original error: {}"
    }
    def __init__(self, pluglinUUID: str, originalTraceback: str):
        super().__init__(self.MESSAGES[getLanguage()].\
                format(pluglinUUID, originalTraceback))
