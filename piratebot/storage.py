import peewee

database = peewee.SqliteDatabase('./data.db')


class BaseModel(peewee.Model):
    """
    Base model for all the other models.
    """
    class Meta:
        database = database
