from discord.ext import commands
import discord

import config

class Union(commands.AutoShardedBot):
    def __init__(self):
        super().__init__(command_prefix='!')

    async def on_ready(self):
        print(f'Logged in as {self.user} ({self.user.id})')

    def run(self):
        super().run(config.token, reconnect=True)
