from peewee import (Model, CharField, IntegerField, AutoField, DateTimeField, JSONField)



class User(Model):
    id = AutoField()

    username = CharField(unique=True)
    password = CharField()

    nickname = CharField()

    level = IntegerField()

    createdAt = DateTimeField()

    lastLoginAt = DateTimeField(null=True)
    lastLoginDevice = CharField(null=True)

    class Meta:
        table_name = 'users'



TABLES = [
    User
]








