import json
import pathlib
import traceback

import aiohttp
import typing
from discord.ext import commands
from discord.ext.commands import CommandError, CheckFailure, UserInputError, \
    DisabledCommand, CommandOnCooldown, NotOwner, NoPrivateMessage, CommandInvokeError, \
    CommandNotFound

from union.core.context import Context


class Union(commands.AutoShardedBot):
    """
    The core bot class.
    """
    no_default = object()

    def __init__(self, config: dict):
        #: The current bot's internal config.
        self.config = config
        super().__init__(command_prefix=self.config.get("command_prefix", '!'))

        #: If this bot is in development mode.
        self.dev = self.config.get("dev", False)

        #: If this bot is a standalone bot (i.e. not running inside of an FAI node).
        self.standalone = self.config.get("standalone", False)

        self.session = aiohttp.ClientSession(loop=self.loop)

        for cog in self.config.get('cogs', []):
            print(f"Loading cog {cog}...")
            try:
                self.load_extension(cog)
            except Exception as ex:
                print(f"Failed to load cog: {cog}")
                traceback.print_exception(type(ex), ex, ex.__traceback__)

    def __del__(self):
        self.session.close()

    async def get_config(self, realm: str, key: str, *, default: typing.Any = no_default):
        """
        Gets a config value.

        :param realm: The realm of storage (usually the cog name).
            Passing None will load from internal configuration (usually not needed).

        :param key: The config key to get.
        :param default: The default value to get.
        """
        if self.standalone:
            if self.dev:
                config_data = pathlib.Path("cog-config-dev.json")
            else:
                config_data = pathlib.Path("cog-config.json")

            data = json.loads(config_data.read_text())
        else:
            # TODO: Implement CNT config receiving
            raise NotImplementedError

        try:
            return data[realm][key]
        except KeyError:
            # check for sentinel instead of None as default
            if default is self.no_default:
                raise

            return default

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
            if not self.dev:
                message = f"\N{SQUARED SOS} An internal error has occurred."
                traceback.print_exception(type(exception.__cause__), exception.__cause__,
                                          exception.__cause__.__traceback__)
            else:
                fmtted = traceback.format_exception(type(exception.__cause__),
                                                    exception.__cause__,
                                                    exception.__cause__.__traceback__)

                # hack for f-strings
                newline = '\n'
                message = f"```py\n{newline.join(fmtted)}"
        else:
            message = f"\N{BLACK QUESTION MARK ORNAMENT} An unknown error has occurred."
            traceback.print_exception(type(exception), exception, exception.__traceback__)

        await context.send(message)

    async def on_ready(self):
        print(f"Logged in as {self.user} ({self.user.id})")

    async def process_commands(self, message):
        ctx = await self.get_context(message, cls=Context)

        if not ctx.command:
            return

        await self.invoke(ctx)

    def run(self):
        super().run(self.config["token"], reconnect=True)
