import os

from source.client import client

from source.storage import database
from source.models.product import Product, Category


def initialize():
    database.connect()
    database.create_tables([Category, Product], safe=True)
    database.close()

    client.run(os.getenv('BOT_TOKEN'))


if __name__ == '__main__':
    initialize()
