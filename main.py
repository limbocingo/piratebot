import os

from piratebot.client import PirateBot

from piratebot.storage import database
from piratebot.commands.store.models import Product, Category

# All the models that are create have
# to be registered in here.
MODELS = [
    Product,
    Category
]


def initialize():
    # Connect to the database and create the tables
    # for the models.
    database.connect()
    database.create_tables(MODELS, safe=True)
    database.close()

    # Run the bot with the token specified in the ENV.
    PirateBot().run(os.getenv('BOT_TOKEN'))


if __name__ == '__main__':
    initialize()
