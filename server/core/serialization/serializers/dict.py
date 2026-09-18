
from .list import ListSerializer


class DictSerializer(ListSerializer):
    typeId = 8
    pythonType = dict

    def serialize(self, value: dict) -> bytes: #type: ignore
        dictList = []

        for k, v in value.items():
            dictList.append(k)
            dictList.append(v)

        return super().serialize(dictList)

    def deserialize(self, data: bytes) -> dict: #type: ignore
        dictList = super().deserialize(data)

        return dict(zip(dictList[::2], dictList[1::2]))

