from .console import handler as consoleHandler
from ..handlerManager import HandlerManager

handlerManager = HandlerManager()

handlerManager.extend(consoleHandler)





