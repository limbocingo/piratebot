import discord
import discord.app_commands

from piratebot.commands.contact.buttons import QuizButton
from piratebot.commands.contact.views import ContactView
from piratebot.commands.contact.modals import ContactModal

from piratebot.util.messages import Messages


class Contact(discord.app_commands.Group):

    def __init__(self, client: discord.Client):
        super().__init__(default_permissions=discord.Permissions(administrator=True))
        self.client = client

    @ discord.app_commands.command(description="Setup the contact channel.")
    async def setup(self, interaction: discord.Interaction):
        await interaction.channel.send(
            embed=discord.Embed(
                title='✉️ — Contact',
                description=Messages(
                    ['commands', 'contact', 'setup']).get_string(),
                color=discord.Color.blurple()
            ),
            view=ContactView(
                QuizButton(
                    ContactModal())),
        )
        await interaction.response.send_message(f'<:management:1233543529847062600> — contact sucessfully initialized!', ephemeral=True)
