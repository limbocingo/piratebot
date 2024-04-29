from peewee import (
    TextField,
    CharField,
    IntegerField,
    ForeignKeyField
)

from piratebot.storage import BaseModel


class Category(BaseModel):
    name = CharField(null=False, max_length=16, unique=True)
    description = CharField(null=False, max_length=82, unique=True)
    image = TextField(null=False)


class Product(BaseModel):
    user = TextField(null=False)
    sold = IntegerField(null=False, default=0)

    category = ForeignKeyField(Category, field='name', on_delete='CASCADE')
    name = CharField(null=False, max_length=16, unique=True)
    description = CharField(null=False, max_length=82, unique=True)
    image = TextField(null=False)
