from peewee import (
    TextField,
    CharField,
    IntegerField,
    ForeignKeyField
)

from piratebot.storage import BaseModel


class Category(BaseModel):
    """
    Category of products.
    """
    name = CharField(null=False, max_length=16, unique=True)
    description = CharField(null=False, max_length=82, unique=True)
    image = TextField(null=False)


class Product(BaseModel):
    """
    Products of the category.
    """
    user = TextField(null=False, unique=True)
    sold = IntegerField(null=False, default=0)

    category = ForeignKeyField(Category, field='name', on_delete='CASCADE')
    name = CharField(null=False, max_length=16, unique=True)
    description = CharField(null=False, max_length=82, unique=True)
    image = TextField(null=False)
