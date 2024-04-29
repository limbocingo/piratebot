import discord
import discord.ui

from piratebot.commands.contact.buttons import CloseButton
from piratebot.commands.contact.views import ContactView

from piratebot.util.messages import Messages


class ContactModal(discord.ui.Modal, title='📧 — Contact'):
    name = discord.ui.TextInput(label='Title.', max_length=16)
    description = discord.ui.TextInput(
        label='What the problem is?', style=discord.TextStyle.paragraph)

    def __init__(self) -> None:
        super().__init__(timeout=None)

    async def create_ticket(self, interaction: discord.Interaction):
        thread = await interaction.channel.create_thread(
            name=f'{self.name} - {interaction.user.id}',
            invitable=False,
            type=discord.ChannelType.private_thread
        )

        await thread.add_user(interaction.user)
        for member in interaction.guild.members:
            if not member.guild_permissions.administrator:
                continue
            await thread.add_user(member)

        return thread.id

    async def on_submit(self, interaction: discord.Interaction):
        thread_id = await self.create_ticket(interaction)
        thread = interaction.guild.get_channel_or_thread(thread_id)

        await thread.send(
            embed=discord.Embed(
                title=self.name,
                description=Messages(
                    ['commands', 'contact', 'ticket']).get_string({'description': self.description,
                                                                   'demandant': interaction.user.id})
            ),
            view=ContactView(CloseButton(
                interaction.guild.get_emoji(1233543524264316969)))
        )
