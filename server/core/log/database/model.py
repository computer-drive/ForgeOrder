from peewee import (Model,
    IntegerField, CharField, JSONField, ForeignKeyField, BlobField
)

class BaseModel(Model):
    pass

class Logs(BaseModel):
    time = IntegerField(primary_key=True) 

    process = CharField()
    level = IntegerField()
    category = CharField()
    action = CharField()
    data = JSONField(null=True)

    message = BlobField(null=True)

    requestId = CharField(null=True)

    class Meta:
        table_name = 'logs_template' # 占位符，实际不会使用

class LogIndex(BaseModel):

    date = CharField(unique=True)
    name = CharField(unique=True)

    first = IntegerField()
    last = IntegerField()

    count = IntegerField(default=0,)

    class Meta:
        table_name = 'logIndex'










    

    
    
    
        