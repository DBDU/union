from discord.ext import commands


class Union(commands.AutoShardedBot):
    def __init__(self, config):
        self.config = config

        super().__init__(command_prefix=self.config.get("command_prefix", "!"))

    async def on_ready(self):
        print(f'Logged in as {self.user} ({self.user.id})')

    def run(self):
        super().run(self.config["token"], reconnect=True)
