import discord
import discord.app_commands
import peewee

from piratebot.commands._store.items import Category, Product
from piratebot.commands._store.items import StoreView


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

    @ discord.app_commands.command(description='Set in what channel the store of the server will be put.')
    async def setup(self, interaction: discord.Interaction) -> None:
        if len(Category.select().dicts()) <= 0:
            return await interaction.response.send_message(f'<:error:1233547139989114891> — no category found, create one first.', ephemeral=True)

        embeded = discord.Embed(
            title='🏛️ — Store',
            description='''Welcome to the Pirate Service 97® Store.


⁍ **What is this?**

    Here you have all the products that we sell. Everything that we can offer
    here it will be waiting for you to be bought.

⁍ **How do I buy?**

    First of all open the menu that is below this message, then select
    any category that you want to see the products of and choose
    the product you like the most and a thread will be openned inside this
    same channel. Finally wait for someone of our staff to attend you.

⁍ **Payment methods**

    The payment methods we currently accept are the next:

    » <:paypal:1233733969548415088> PayPal
    » <:ethereum:1233733991354597496> Ethereum
    » <:bitcoin:1233733977865584721> Bitcoin
    » <:usd:1233733973188804721> USDC

*When is treated with clients we follow the [Safety & Rules](https://discord.com/channels/1233089093617975386/1233100415231590481/1233717081342611487).
Its very recommended reading that before buying from us or doing a trade.*''',
            color=discord.Color.gold()
        )

        await interaction.channel.send(embed=embeded, view=StoreView(categories=[discord.SelectOption(label='No Selection', description='No selection currently made.', default=True)] + [
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

    #
    # Products
    #

    async def products(self, interaction: discord.Interaction, current: str):
        return [discord.app_commands.Choice(name=product['name'], value=product['name'])
                for product in Product.select().dicts()]

    @ add.command(description='Add a product. The max of products is 10 per category.')
    @ discord.app_commands.describe(name="Name of the product.")
    @ discord.app_commands.describe(description="What is about.")
    @ discord.app_commands.describe(image="ID of a emoji, that will be the image.")
    @ discord.app_commands.describe(category="Category where you want to store the product.")
    @ discord.app_commands.autocomplete(category=categories)
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
