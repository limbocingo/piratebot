import importlib
import inspect
import os

import discord
import discord.app_commands

from source.styles import Color, Log


class PirateBot(discord.Client):
    """
    Client of the PirateBot bot.
    """

    def __init__(self) -> None:
        super().__init__(intents=discord.Intents.all())

        self.tree = discord.app_commands.CommandTree(self)
        self.__add_commands()

    def __add_commands(self):
        files = os.listdir('source/commands/')
        for file in files:
            if file[-3:] != '.py':
                continue

            if file == '__init__.py':
                continue

            lib = importlib.import_module('source.commands.' + file[:-3])
            members = inspect.getmembers(lib)

            for name, member in members:
                if not inspect.isclass(member):
                    continue

                if not issubclass(member, discord.app_commands.Group):
                    continue

                self.tree.add_command(
                    member(self), guild=discord.Object(id=1233089093617975386))
                Log('pirate.client', f'Command ({name})').information()
        print()

    async def on_ready(self):
        print()

        Log('pirate.client', f'Booting up: {Color.GREEN.value}{
            self.application_id}').information()

        await self.tree.sync(guild=self.get_guild(1233089093617975386))
        Log('pirate.client', f'Synced with guild: {
            Color.GREEN.value}1233089093617975386').information()


client = PirateBot()