from typing import Any
import os

from .schema import SCHEMA, KEYS
from core.binpack import BinParser

class BinInfo:

    def __init__(self, path: str):
        self.path = path    

        self.parser = None

    def load(self):
        if self.parser is not None:
            return

            

        with open(self.path, "rb") as f:
            self.parser = BinParser(SCHEMA).parseFile(f)

    def __getitem__(self, key: str):
        if self.parser is None:
            self.load()

        return self.parser[key] #type: ignore

    def __setitem__(self, key: str, value: Any):
        if self.parser is None:
            self.load()

        self.parser[key] = value #type: ignore


    def save(self):
        if self.parser is None:
            raise ValueError("BinInfo is not loaded")

        with open(self.path, "wb") as f:
            self.parser.saveFile(f)

if not os.path.exists("state.dat"):
    with open("state.dat", "w") as f:
        f.write("")

BIN_INFO_PATH = "state.dat"

bininfo = BinInfo(BIN_INFO_PATH)

    


