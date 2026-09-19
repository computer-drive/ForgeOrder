from dataclasses import dataclass, field

from ..plugins.schema import PluginInfo
from core.serialization.serializers.custom import ProxySerializer
from core.serialization.manager import useSerializer



@dataclass
class Schema:
    isFirstStart : bool = False
    isNormalShutdown : bool = False
    lastStartTimestamp : int = 0
    startupCount : int = 0
    config : str = "data/config.json"

    plugins: list[PluginInfo] = field(default_factory=list)

serializerManager = useSerializer()

serializerManager.register(
            ProxySerializer(
                            101, Schema, dict, 
                lambda x: {attr: getattr(x, attr) for attr in dir(x) if not attr.startswith("__")},
                lambda x: Schema(**x),
            )
        )
serializerManager.register(
            ProxySerializer(
                102, PluginInfo, dict, 
                lambda x: x.toDict(),
                lambda x: PluginInfo(**x),
            )
)
