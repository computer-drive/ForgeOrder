from dataclasses import dataclass

@dataclass(eq=False)
class PluglinInfo:
    uuid: str
    path: str
    hashes: dict[str, str]

    def __eq__(self, other):
        if not isinstance(other, PluglinInfo):
            return NotImplemented
        return self.uuid == other.uuid

    def __hash__(self):
        return hash(self.uuid)

    

    def toDict(self) -> dict:
        return {
            "uuid": self.uuid,
            "path": self.path,
            "hashes": self.hashes,
        }

PLUGLIN_PATH = "data/plugins/"
