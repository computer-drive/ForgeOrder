
from peewee import Database

class SettingsService:

    def __init__(self, database: Database):
        self.database = database

    def initalize(self):
        pass