import discord
import discord.ui.item


class StoreView(discord.ui.View):
    """
    The view for the store.
    """

    def __init__(self, item: discord.ui.item.Item) -> None:
        super().__init__(timeout=None)
        self.add_item(item=item)


class ProductView(discord.ui.View):
    """
    Product thread message view.
    """

    def __init__(self, buttons: list[discord.ui.Button]) -> None:
        super().__init__(timeout=None)
        for button in buttons:
            self.add_item(button)
