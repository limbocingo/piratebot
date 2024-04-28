import discord
import discord.app_commands


class Channel(discord.app_commands.Group):

    def __init__(self, client: discord.Client):
        super().__init__(default_permissions=discord.Permissions(administrator=True))
        self.client = client

    @ discord.app_commands.command(description='Set in what channel the store of the server will be put.')
    async def delete(self, interaction: discord.Interaction) -> None:
        await interaction.channel.purge(limit=100)
        await interaction.response.send_message(f'<:management:1233543529847062600> — channel nuked.', ephemeral=True)
