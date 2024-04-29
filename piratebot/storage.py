import peewee

# Local database used to store all the user information.
database = peewee.SqliteDatabase('./resources/pirateservice.db')


class BaseModel(peewee.Model):
    class Meta:
        database = database
