from peewee import (Model, CharField, IntegerField, BlobField)
class Settings(Model):
    id = IntegerField(primary_key=True)

    name = CharField()
    value = BlobField()
    
    class Meta:
        table_name = 'settings'