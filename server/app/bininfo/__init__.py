from typing import Any
import os

from core.serialization import useSerializer
from core.serialization.serializers.custom import ProxySerializer
from .schema import Schema

class BinInfo:

    def __init__(self, path: str):
        self.path = path    


        self.data : Schema = None

        self.serializer = useSerializer()
        

    def load(self):
        if self.data is not None:
            return

        with open(self.path, "rb") as f:
            fileData = f.read()

        if fileData:
            self.data = self.serializer.deserialize(fileData)
            # print(self.data)
        else:
            self.data = Schema()

    

    def save(self):
        if self.data is None:
            raise ValueError("BinInfo is not loaded")
        
        # print(self.data)

        with open(self.path, "wb") as f:
            f.write(self.serializer.serialize(self.data))

if not os.path.exists("state.dat"):
    with open("state.dat", "w") as f:
        f.write("")

BIN_INFO_PATH = "state.dat"

bininfo = BinInfo(BIN_INFO_PATH)

    


