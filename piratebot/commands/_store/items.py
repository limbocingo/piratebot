import datetime

import asyncio
import discord
import discord.app_commands

from piratebot.commands._store.models import Category, Product


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


class Categories(discord.ui.Select):
    """
    Category selector
    """

    def __init__(self, categories: list[discord.SelectOption]):
        super().__init__(placeholder="Select the category you preffer.",
                         max_values=1, min_values=1, options=categories)

    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == 'No Selection':
            return await interaction.response.send_message(content='...', ephemeral=True)

        if len(Product.select().dicts()) <= 0:
            return await interaction.response.send_message(f'<:error:1233547139989114891> — no product found in this category.', ephemeral=True)

        embeded = discord.Embed(
            title=f'🏛️ — Store > {
                self.values[0]} > Products',

            description='''
Select any product you preffer and a thread will be created
in this same channel.

*When is treated with clients we follow the [Safety & Rules](https://discord.com/channels/1233089093617975386/1233100415231590481/1233717081342611487).
Its very recommended reading that before buying from us or doing a trade.*''',

            color=discord.Color.gold()
        )

        products = [
            discord.SelectOption(label='No Selection', description='No selection currently made.', default=True)] + [
            discord.SelectOption(
                label=category['name'], description=category['description'],
                emoji=interaction.guild.get_emoji(int(category['image'])))
            for category in Product.select().where(Category.get(Category.name == self.values[0])).dicts()
        ]

        await interaction.response.send_message(embed=embeded, view=StoreView(products=products), ephemeral=True)


class Products(discord.ui.Select):
    """
    Product selector.
    """

    def __init__(self, products: list[discord.SelectOption]):
        super().__init__(placeholder="Select the option you preffer.",
                         max_values=1, min_values=1, options=products)

    def has_admin(self, member: discord.Member):
        for role in member.roles:
            if not role.permissions.administrator:
                continue
            return True

    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == 'No Selection':
            return await interaction.response.send_message(content='...', ephemeral=True)

        if len(interaction.channel.threads) > 15:
            return await interaction.response.send_message(f'<:error:1233547139989114891> — oops, seems like we have already a lot of petitions, come back later.', ephemeral=True)

        for thread in interaction.channel.threads:
            if thread.name.split(' ')[-1] != str(interaction.user.id):
                continue
            return await interaction.response.send_message(f'<:error:1233547139989114891> — you are already buying something.', ephemeral=True)

        thread = await interaction.channel.create_thread(name=f'{self.values[0]} - {interaction.user.id}', invitable=False, type=discord.ChannelType.private_thread)
        await thread.add_user(interaction.user)

        seller = int(Product.get(
            Product.name == self.values[0]).user)
        await thread.add_user(interaction.guild.get_member(seller))

        for member in interaction.guild.members:
            if not member.guild_permissions.administrator:
                continue
            await asyncio.sleep(0.75)
            await thread.add_user(member)

        product = Product.get(Product.name == self.values[0])

        embeded = discord.Embed(
            title=f'<:{interaction.guild.get_emoji(
                int(product.image)).name}:{product.image}> → ' + self.values[0],
            description=f'''

> <:newmember:1233543528320335932> · <@{product.user}> (Seller)
> <:member:1233543548532424794> · <@{interaction.user.id}> (Buyer)

> <:info:1233543525585391616> · Description
```
{product.description}
```
''',
            timestamp=datetime.datetime.today()
        )

        thread_view = discord.ui.View(timeout=None)
        sold = discord.ui.Button(
            style=discord.ButtonStyle.blurple,
            label='Sold',
            emoji=interaction.guild.get_emoji(1233745604367224863)
        )
        close = discord.ui.Button(
            style=discord.ButtonStyle.red,
            label='Close',
            emoji=interaction.guild.get_emoji(1233543524264316969)
        )

        close.callback = self.on_close
        sold.callback = self.on_sold

        thread_view.add_item(close)
        thread_view.add_item(sold)

        await thread.send(embed=embeded, view=thread_view)

    async def on_close(self, interaction: discord.Interaction):
        await interaction.channel.delete()

    async def on_sold(self, interaction: discord.Interaction):
        if not self.has_admin(interaction.user):
            return await interaction.response.send_message(f'<:error:1233547139989114891> — you can not do that.', ephemeral=True)

        name = interaction.channel.name.rsplit(' ', maxsplit=2)[0]
        product = Product.get(Product.name == name)

        update = Product.update(
            sold=product.sold + 1).where(Product.name == product.name)
        update.execute()

        await interaction.channel.delete()
