import discord
import discord.ui

from piratebot.commands.store.models import Product


def has_admin(member: discord.Member) -> bool:
    for role in member.roles:
        if not role.permissions.administrator:
            continue
        return True


class SoldProductButton(discord.ui.Button):

    def __init__(self, product: Product, emoji: discord.Emoji):
        super().__init__(style=discord.ButtonStyle.blurple,
                         label=product.name,
                         emoji=emoji
                         )
        self.product = product

    async def callback(self, interaction: discord.Interaction) -> None:
        if not has_admin(interaction.user):
            return await interaction.response.send_message(f'<:error:1233547139989114891> — you can not do that.', ephemeral=True)

        update = Product.update(
            sold=self.product.sold + 1).where(Product.name == self.product.name)
        update.execute()

        await interaction.channel.delete()
