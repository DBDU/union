import traceback

from discord.ext import commands
from discord.ext.commands import Context, CommandError, CheckFailure, UserInputError, \
    DisabledCommand, CommandOnCooldown, NotOwner, NoPrivateMessage, CommandInvokeError, \
    CommandNotFound


class Union(commands.AutoShardedBot):
    """
    The core bot class.
    """
    def __init__(self, config: dict):
        #: The current bot's config.
        self.config = config

        super().__init__(command_prefix=self.config.get("command_prefix", '!'))

        for cog in self.config.get('cogs', []):
            print(f"Loading cog {cog}...")
            try:
                self.load_extension(cog)
            except Exception as ex:
                print(f"Failed to load cog: {cog}")
                traceback.print_exception(type(ex), ex, ex.__traceback__)

    async def on_command_error(self, context: Context, exception: CommandError):
        """
        Handles non-fatal command errors.
        """
        # check for commandnotfound before joining args
        # as it saves a few cycles not having to execute the join
        if isinstance(exception, CommandNotFound):
            return

        # joined args are defined here to prevent code duplication
        # rather than in the format strings
        args = ' '.join(exception.args)

        if isinstance(exception, CheckFailure) and not isinstance(exception, NoPrivateMessage):
            message = f"\N{NO ENTRY SIGN} Checks failed: {args}"
        elif isinstance(exception, NoPrivateMessage):
            message = f"\N{CROSS MARK} This command does not work in private messages."
        elif isinstance(exception, UserInputError):
            message = f"\N{CROSS MARK} {args}"
        elif isinstance(exception, DisabledCommand):
            message = f"\N{CROSS MARK} The command {context.invoked_with} is disabled."
        elif isinstance(exception, CommandOnCooldown):
            message = f"\N{CROSS MARK} The command {context.invoked_with} is on cooldown. " \
                      f"Try again in {exception.retry_after:.2f} seconds."
        elif isinstance(exception, NotOwner):
            message = f"\N{NO ENTRY SIGN} You are not the bot owner."
        elif isinstance(exception, CommandInvokeError):
            # TODO: Perhaps handle this better?
            message = f"\N{SQUARED SOS} An internal error has occurred."
            traceback.print_exception(type(exception.__cause__), exception.__cause__,
                                      exception.__cause__.__traceback__)
        else:
            message = f"\N{BLACK QUESTION MARK ORNAMENT} An unknown error has occurred."
            traceback.print_exception(type(exception), exception, exception.__traceback__)

        await context.send(message)

    async def on_ready(self):
        print(f"Logged in as {self.user} ({self.user.id})")

    def run(self):
        super().run(self.config["token"], reconnect=True)
