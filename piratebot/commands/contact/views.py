import discord
import discord.ui


class ContactView(discord.ui.View):

    def __init__(self, item: discord.ui.item.Item) -> None:
        super().__init__(timeout=None)
        self.add_item(item=item)
