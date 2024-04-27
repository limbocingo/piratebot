import peewee

import discord
import discord.app_commands

from source.models.product import Category, Product


class Categories(discord.ui.Select):
    """
    Category selector
    """

    def __init__(self, categories: list[discord.SelectOption]):
        super().__init__(placeholder="Select the category you preffer.",
                         max_values=1, min_values=1, options=categories)

    async def callback(self, interaction: discord.Interaction):
        embed = discord.Embed()

        await interaction.channel.send(embed=embed, view=StoreView(products=[
            discord.SelectOption(
                label=category['name'], description=category['description'],
                emoji=interaction.guild.get_emoji(int(category['image'])))
            for category in Product.select().where(Category.get(Category.name == self.values[0])).dicts()
        ]))


class Products(discord.ui.Select):
    """
    Product selector.
    """

    def __init__(self, products: list[discord.SelectOption]):
        super().__init__(placeholder="Select the option you preffer.",
                         max_values=1, min_values=1, options=products)


class StoreView(discord.ui.View):
    """
    The view for the store.
    """

    def __init__(self, categories: list[discord.SelectOption] = None, products: list[discord.SelectOption] = None):
        super().__init__(timeout=None)

        if not categories and not products:
            raise ValueError('No category or product gave.')

        if categories:
            self.add_item(Categories(categories))
            return

        self.add_item(Products(products))


class Store(discord.app_commands.Group):
    """
    Pirate Service store manager.
    """

    add = discord.app_commands.Group(
        name="add", description="Add something into the store database.")
    remove = discord.app_commands.Group(
        name="remove", description="Remove something into the store database.")

    def __init__(self, client: discord.Client):
        super().__init__(default_permissions=discord.Permissions(administrator=True))
        self.client = client

    @discord.app_commands.command(description='Set in what channel the store of the server will be put.')
    async def initialize(self, interaction: discord.Interaction) -> None:
        await interaction.channel.send("hello from the subcommand!", view=StoreView(categories=[
            discord.SelectOption(
                label=category['name'], description=category['description'],
                emoji=interaction.guild.get_emoji(int(category['image'])))
            for category in Category.select().dicts()
        ]))
        await interaction.response.send_message(f'<:management:1233543529847062600> — store sucessfully intialized!', ephemeral=True)

    #
    # Categories
    #

    async def categories(self, interaction: discord.Interaction, current: str):
        return [discord.app_commands.Choice(name=category['name'], value=category['name'])
                for category in Category.select().dicts()]

    @add.command(description='Add a category. The max of categories is 10.')
    @discord.app_commands.describe(name="Name of the category.")
    @discord.app_commands.describe(description="What is about.")
    @discord.app_commands.describe(image="ID of a emoji, that will be the image.")
    async def category(self, interaction: discord.Interaction, name: str, image: str, description: str):
        if len(Category.select().dicts()) > 10:
            return await interaction.response.send_message(f'<:error:1233547139989114891> — there are already `10` categories.', ephemeral=True)

        if not interaction.guild.get_emoji(int(image)):
            return await interaction.response.send_message(f'<:error:1233547139989114891> — `{image}` is not a valid emoji inside your server.', ephemeral=True)

        category = Category(name=name, image=image, description=description)
        try:
            category.save()
        except peewee.IntegrityError:
            return await interaction.response.send_message(f'<:error:1233547139989114891> — `{name}` not valid `name` or `description`.', ephemeral=True)

        await interaction.response.send_message(f'<:management:1233543529847062600> — `{name}` added into `store` categories.', ephemeral=True)

    @remove.command(description='Remove a category.')
    @discord.app_commands.describe(name="Name of the category.")
    @discord.app_commands.autocomplete(name=categories)
    async def category(self, interaction: discord.Interaction, name: str):
        try:
            category = Category.get(Category.name == name)
        except peewee.DoesNotExist:
            return await interaction.response.send_message(f'<:error:1233547139989114891> — `{name}` is not a valid name.', ephemeral=True)
        category.delete_instance()

        await interaction.response.send_message(f'<:delete:1233543524264316969> — `{name}` deleted from `store` categories.', ephemeral=True)

    #
    # Products
    #

    async def products(self, interaction: discord.Interaction, current: str):
        return [discord.app_commands.Choice(name=product['name'], value=product['name'])
                for product in Product.select().dicts()]

    @add.command(description='Add a product. The max of products is 10 per category.')
    @discord.app_commands.describe(name="Name of the product.")
    @discord.app_commands.describe(description="What is about.")
    @discord.app_commands.describe(image="ID of a emoji, that will be the image.")
    @discord.app_commands.describe(category="Category where you want to store the product.")
    @discord.app_commands.autocomplete(category=categories)
    async def product(self, interaction: discord.Interaction, name: str, image: str, description: str, category: str):
        if len(Product.select().dicts()) > 10:
            return await interaction.response.send_message(f'<:error:1233547139989114891> — there are already `10` products.', ephemeral=True)

        if not Category.select().where(Category.name == category).exists():
            return await interaction.response.send_message(f'<:error:1233547139989114891> — `{category}` is not a valid category.', ephemeral=True)

        if not interaction.guild.get_emoji(int(image)):
            return await interaction.response.send_message(f'<:error:1233547139989114891> — `{image}` is not a valid emoji inside your server.', ephemeral=True)

        product = Product(user=interaction.user.id, name=name, image=image, description=description,
                          category=Category.get(Category.name == category))

        try:
            product.save()
        except peewee.IntegrityError:
            return await interaction.response.send_message(f'<:error:1233547139989114891> — `{name}` not valid `name` or `description`.', ephemeral=True)

        await interaction.response.send_message(f'<:management:1233543529847062600> — `{name}` product added into `{category}`.', ephemeral=True)

    @remove.command(description='Remove a product inside a category.')
    @discord.app_commands.describe(name="Name of the product.")
    @discord.app_commands.autocomplete(name=products)
    async def product(self, interaction: discord.Interaction, name: str):
        try:
            product = Product.get(Product.name == name)
        except peewee.DoesNotExist:
            return await interaction.response.send_message(f'<:error:1233547139989114891> — `{name}` is not a valid name.', ephemeral=True)
        product.delete_instance()

        await interaction.response.send_message(f'<:delete:1233543524264316969> — `{name}` deleted from `store` categories.', ephemeral=True)
