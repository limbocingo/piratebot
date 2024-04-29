import datetime

import discord
import discord.app_commands

from piratebot.commands.store.models import Category, Product
from piratebot.commands.store.views import StoreView, ProductView
from piratebot.commands.store.buttons import SoldProductButton, CloseProductButton

from piratebot.util.messages import Messages


class CategorySelector(discord.ui.Select):

    def __init__(self, categories: list[discord.SelectOption]):
        super().__init__(placeholder="Select the category you preffer.",
                         max_values=1, min_values=1, options=categories)

    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == 'No Selection':
            return await interaction.response.send_message(content='...', ephemeral=True)

        if len(Product.select().dicts()) <= 0:
            return await interaction.response.send_message(f'<:error:1233547139989114891> — no product found in this category.', ephemeral=True)

        await interaction.response.send_message(
            embed=discord.Embed(
                title=f'🏛️ — Store > {
                    self.values[0]} > Products',
                description=Messages(
                    ['commands', 'store', 'product', 'selection']).get_string(),
                color=discord.Color.gold()
            ),
            view=StoreView(
                item=ProductSelector(
                    products=[
                        discord.SelectOption(
                            label='No Selection',
                            description='No selection currently made.',
                            default=True)
                    ] + [
                        discord.SelectOption(
                            label=product['name'],
                            description=product['description'],
                            emoji=interaction.guild.get_emoji(int(product['image'])))
                        for product in Product.select().where(
                            Product.category == Category.get(
                                Category.name == self.values[0])
                        ).dicts()
                    ])),
            ephemeral=True
        )


class ProductSelector(discord.ui.Select):

    def __init__(self, products: list[discord.SelectOption]):
        super().__init__(placeholder="Select the option you preffer.",
                         max_values=1, min_values=1, options=products)

    def has_thread_open(self, interaction: discord.Interaction, member: discord.Member):
        for thread in interaction.channel.threads:
            if thread.name.split(' ')[-1] != str(interaction.user.id):
                continue
            return True

    async def create_ticket(self, interaction: discord.Interaction):
        thread = await interaction.channel.create_thread(
            name=f'{self.values[0]} - {interaction.user.id}', invitable=False, type=discord.ChannelType.private_thread
        )

        await thread.add_user(interaction.user)
        await thread.add_user(interaction.guild.get_member(
            int(Product.get(Product.name == self.values[0]).user)
        ))

        for member in interaction.guild.members:
            if not member.guild_permissions.administrator:
                continue
            await thread.add_user(member)

        return thread.id

    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == 'No Selection':
            return await interaction.response.send_message(content='...', ephemeral=True)

        if len(interaction.channel.threads) > 15:
            return await interaction.response.send_message(f'<:error:1233547139989114891> — oops, seems like we have already a lot of petitions, come back later.', ephemeral=True)

        if self.has_thread_open(interaction, interaction.user.id):
            return await interaction.response.send_message(f'<:error:1233547139989114891> — you are already buying something.', ephemeral=True)

        product = Product.get(Product.name == self.values[0])
        ticket = await self.create_ticket(interaction)

        await interaction.guild.get_thread(ticket).send(
            embed=discord.Embed(
                title=f'<:{interaction.guild.get_emoji(
                    int(product.image)).name}:{product.image}> → {self.values[0]}',
                description=Messages(['commands', 'store', 'product', 'thread']
                                     ).get_string(
                                         {
                                             'seller': product.user,
                                             'buyer': interaction.user.id,
                                             'description': product.description
                                         }
                ),
                timestamp=datetime.datetime.today()
            ),
            view=ProductView(
                [SoldProductButton(product=product,
                                   emoji=interaction.guild.get_emoji(1233745604367224863)),
                 CloseProductButton(emoji=interaction.guild.get_emoji(1233543524264316969))]
            )
        )
