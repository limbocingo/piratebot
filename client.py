import os
import discord


class PirateBot(discord.Client):
    
    async def on_ready(self):
        print(f'Logged on as {self.application_id}!')

    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}')

client = PirateBot(intents=discord.Intents.all())
client.run(os.getenv('BOT_TOKEN'))
