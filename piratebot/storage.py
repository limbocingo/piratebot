import peewee

# Local database used to store all the user information.
database = peewee.SqliteDatabase('./resources/pirateservice.db')


class BaseModel(peewee.Model):
    """
    Base model for all the other models.
    """
    class Meta:
        database = database
