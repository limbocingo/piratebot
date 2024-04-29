import discord
import discord.ui


class CloseButton(discord.ui.Button):

    def __init__(self, emoji: discord.Emoji):
        super().__init__(style=discord.ButtonStyle.gray,
                         label='Close',
                         emoji=emoji
                         )

    def has_admin(member: discord.Member) -> bool:
        for role in member.roles:
            if not role.permissions.administrator:
                continue
            return True

    async def callback(self, interaction: discord.Interaction) -> None:
        if not self.has_admin(interaction.user):
            return await interaction.response.send_message(f'<:error:1233547139989114891> — you can not do that.', ephemeral=True)

        await interaction.channel.delete()


class QuizButton(discord.ui.Button):

    def __init__(self, modal: discord.ui.Modal):
        super().__init__(style=discord.ButtonStyle.secondary,
                         label='Get in Contact!', emoji='📧')
        self.modal = modal

    async def callback(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_modal(self.modal)
