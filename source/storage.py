import peewee


database = peewee.SqliteDatabase('./data.db')


class BaseModel(peewee.Model):
    class Meta:
        database = database
