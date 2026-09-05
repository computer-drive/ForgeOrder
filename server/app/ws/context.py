from dataclasses import dataclass
from multiprocessing.connection import Connection

from ..processing.log import WorkerLogger
from ..config import ConfigManager


@dataclass
class WebsocketServerContext:
    pipe: Connection
    logger: WorkerLogger
    config: ConfigManager
