from typing import Any
from ....utils.common import getLanguage


class ContextAccessError(Exception):
    MESSAGES = {
        "en": "Cannot get value from context, context must provide a get() method",
        "zh": "不能从上下文中取值，上下文对象必须实现一个get()方法"
    }
    def __init__(self, context: Any):
        self.context = context

        super().__init__(self.MESSAGES[getLanguage()])
