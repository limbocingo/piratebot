import discord
import discord.app_commands

from piratebot.util.messages import Messages


class Contact(discord.app_commands.Group):

    def __init__(self, client: discord.Client):
        super().__init__(default_permissions=discord.Permissions(administrator=True))
        self.client = client

    @ discord.app_commands.command(description="Setup the contact channel.")
    async def setup(self, interaction: discord.Interaction):
        await interaction.channel.send(
            embed=discord.Embed(
                title='💬 — Contact',
                description=Messages(['commands', 'contact', 'setup']).get_string()
            )
        )
