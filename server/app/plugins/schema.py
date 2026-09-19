from dataclasses import dataclass

@dataclass(eq=False)
class PluginInfo:
    uuid: str
    path: str
    hashes: dict[str, str]

    enabled: bool = True

    def __eq__(self, other):
        if not isinstance(other, PluginInfo):
            return NotImplemented
        return self.uuid == other.uuid

    def __hash__(self):
        return hash(self.uuid)

    

    def toDict(self) -> dict:
        return {
            "uuid": self.uuid,
            "path": self.path,
            "hashes": self.hashes,
            "enabled": self.enabled,
        }

PLUGIN_PATH = "data/plugins/"
