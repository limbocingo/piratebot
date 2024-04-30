import discord
import discord.app_commands
import peewee

from piratebot.commands.store.selectors import CategorySelector, ProductSelector
from piratebot.commands.store.models import Category, Product
from piratebot.commands.store.views import StoreView

from piratebot.util.messages import Messages


class Store(discord.app_commands.Group):
    """
    Pirate Service store manager.
    """

    add = discord.app_commands.Group(
        name="add", description="Add something into the store database.")
    remove = discord.app_commands.Group(
        name="remove", description="Remove something into the store database.")
    edit = discord.app_commands.Group(
        name="edit", description="Edit a category or product.")

    def __init__(self, client: discord.Client):
        super().__init__(default_permissions=discord.Permissions(administrator=True))
        self.client = client

    @ discord.app_commands.command(description='Set in what channel the store of the server will be put.')
    async def setup(self, interaction: discord.Interaction) -> None:
        if len(Category.select().dicts()) <= 0:
            return await interaction.response.send_message(f'<:error:1233547139989114891> — no category found, create one first.', ephemeral=True)

        embeded = discord.Embed(
            title='🏛️ — Store',
            description=Messages(['commands', 'store', 'setup']).get_string(),
            color=discord.Color.gold()
        )

        await interaction.channel.send(embed=embeded, view=StoreView(item=CategorySelector([discord.SelectOption(label='No Selection', description='No selection currently made.', default=True)] + [
            discord.SelectOption(
                label=category['name'], description=category['description'],
                emoji=interaction.guild.get_emoji(int(category['image'])))
            for category in Category.select().dicts()
        ])))
        await interaction.response.send_message(f'<:management:1233543529847062600> — store sucessfully intialized!', ephemeral=True)

    #
    # Categories
    #

    async def categories(self, interaction: discord.Interaction, current: str):
        return [discord.app_commands.Choice(name=category['name'], value=category['name'])
                for category in Category.select().dicts()]

    async def categories_fields(self, interaction: discord.Interaction, current: str):
        return [discord.app_commands.Choice(name=field, value=field)
                for field in list(Category._meta.columns.keys())]

    @ add.command(description='Add a category. The max of categories is 10.')
    @ discord.app_commands.describe(name="Name of the category.")
    @ discord.app_commands.describe(description="What is about.")
    @ discord.app_commands.describe(image="ID of a emoji, that will be the image.")
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

    @ remove.command(description='Remove a category.')
    @ discord.app_commands.describe(name="Name of the category.")
    @ discord.app_commands.autocomplete(name=categories)
    async def category(self, interaction: discord.Interaction, name: str):
        try:
            category = Category.get(Category.name == name)
        except peewee.DoesNotExist:
            return await interaction.response.send_message(f'<:error:1233547139989114891> — `{name}` is not a valid name.', ephemeral=True)
        category.delete_instance()

        await interaction.response.send_message(f'<:delete:1233543524264316969> — `{name}` deleted from `store` categories.', ephemeral=True)

    @ edit.command(description='Edit a product.')
    @ discord.app_commands.describe(name="Name of the product.")
    @ discord.app_commands.describe(field='Field of the product you want to edit.')
    @ discord.app_commands.describe(value='Value of the field.')
    @ discord.app_commands.autocomplete(name=categories)
    @ discord.app_commands.autocomplete(field=categories_fields)
    async def product(self, interaction: discord.Interaction, name: str, field: str, value: str):
        if field not in list(Category._meta.columns.keys()):
            return await interaction.response.send_message(f'<:error:1233547139989114891> — `{name}` is not a valid name.', ephemeral=True)

        (Category
            .update(**{field: value})
            .where(Category.name == name)
            .execute())

        await interaction.response.send_message(f'<:management:1233543529847062600> — `{field}` value changed to `{value}`.', ephemeral=True)

    #
    # Products
    #

    async def products(self, interaction: discord.Interaction, current: str):
        return [discord.app_commands.Choice(name=product['name'], value=product['name'])
                for product in Product.select().dicts()]

    async def products_fields(self, interaction: discord.Interaction, current: str):
        return [discord.app_commands.Choice(name=field, value=field)
                for field in list(Product._meta.columns.keys())]

    @ add.command(description='Add a product. The max of products is 10 per category.')
    @ discord.app_commands.describe(name="Name of the product.")
    @ discord.app_commands.describe(description="What is about.")
    @ discord.app_commands.describe(image="ID of a emoji, that will be the image.")
    @ discord.app_commands.describe(category="Category where you want to store the product.")
    @ discord.app_commands.autocomplete(category=categories)
    async def product(self, interaction: discord.Interaction, name: str, image: str, description: str, category: str):
        if len(Product.select().where(Category == Category.get(name=category)).dicts()) > 10:
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
            return await interaction.response.send_message(f'<:error:1233547139989114891> — `{name}` not valid `name` or `description`. ', ephemeral=True)

        await interaction.response.send_message(f'<:management:1233543529847062600> — `{name}` product added into `{category}`.', ephemeral=True)

    @ remove.command(description='Remove a product inside a category.')
    @ discord.app_commands.describe(name="Name of the product.")
    @ discord.app_commands.autocomplete(name=products)
    async def product(self, interaction: discord.Interaction, name: str):
        try:
            product = Product.get(Product.name == name)
        except peewee.DoesNotExist:
            return await interaction.response.send_message(f'<:error:1233547139989114891> — `{name}` is not a valid name.', ephemeral=True)
        product.delete_instance()

        await interaction.response.send_message(f'<:delete:1233543524264316969> — `{name}` deleted from `store` categories.', ephemeral=True)

    @ edit.command(description='Edit a product.')
    @ discord.app_commands.describe(name="Name of the product.")
    @ discord.app_commands.describe(field='Field of the product you want to edit.')
    @ discord.app_commands.describe(value='Value of the field.')
    @ discord.app_commands.autocomplete(name=products)
    @ discord.app_commands.autocomplete(field=products_fields)
    async def product(self, interaction: discord.Interaction, name: str, field: str, value: str):
        if field not in list(Product._meta.columns.keys()):
            return await interaction.response.send_message(f'<:error:1233547139989114891> — `{name}` is not a valid name.', ephemeral=True)

        (Product
            .update(**{field: value})
            .where(Product.name == name)
            .execute())

        await interaction.response.send_message(f'<:management:1233543529847062600> — `{field}` value changed to `{value}`.', ephemeral=True)
