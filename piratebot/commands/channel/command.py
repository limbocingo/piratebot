import discord
import discord.app_commands


class Channel(discord.app_commands.Group):

    def __init__(self, client: discord.Client):
        super().__init__(default_permissions=discord.Permissions(administrator=True))
        self.client = client

    @ discord.app_commands.command(description='Nuke 100 messages from the channel you are running this.')
    async def nuke(self, interaction: discord.Interaction) -> None:
        await interaction.channel.purge(limit=100)
        await interaction.response.send_message(f'<:management:1233543529847062600> — nuked `100` messages from the channel.', ephemeral=True)

    @ discord.app_commands.command(description='Rename the channel you execute this.')
    @ discord.app_commands.describe(name="New name of the channel.")
    async def rename(self, interaction: discord.Interaction, name: str) -> None:
        await interaction.channel.edit(name=name)
        await interaction.response.send_message(f'<:management:1233543529847062600> — channel <#{interaction.channel.id}> renamed.', ephemeral=True)
