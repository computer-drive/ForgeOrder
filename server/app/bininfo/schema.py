from dataclasses import dataclass

@dataclass
class Schema:
    isFirstStart : bool = False
    isNormalShutdown : bool = False
    lastStartTimestamp : int = 0
    startupCount : int = 0
    config : str = "data/config.json"
