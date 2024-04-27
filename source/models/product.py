from peewee import (
    TextField,
    CharField,
    IntegerField,
    ForeignKeyField,
)

from source.storage import BaseModel


class Category(BaseModel):
    name = CharField(null=False, max_length=16, unique=True)
    description = CharField(null=False, max_length=82, unique=True)
    image = TextField(null=False)


class Product(BaseModel):
    user = TextField(null=False, unique=True)
    sold = IntegerField(null=False, default=0)

    category = ForeignKeyField(Category, field='name')
    name = CharField(null=False, max_length=16, unique=True)
    description = CharField(null=False, max_length=82, unique=True)
    image = TextField(null=False)
