import asyncio

from discord.ext import commands


class Context(commands.Context):
    async def disambiguate(self, items, *, timeout=10):
        """
        Used in converters when multiple matches can be expected.
        """
        # Couldn't think of a way to combine these two
        if len(items) == 0:
            raise commands.BadArgument("No matches found.")

        if len(items) == 1:
            return items[0]

        choices = '\n'.join(f"{i}: {entry}" for i, entry in enumerate(items, start=1))
        await self.send(f"Found multiple matching entries. Please choose the correct one\n{choices}")

        def check(message):
            return (message.content.isnumeric() and
                    message.author == self.author and
                    message.channel == self.channel)

        try:
            message = await self.bot.wait_for("message", check=check, timeout=timeout)
        except asyncio.TimeoutError:
            raise commands.BadArgument("Timeout reached.")

        # We check for numbers only so no try/except required
        index = int(message.content)

        try:
            return items[index - 1]
        except IndexError:
            raise commands.BadArgument("Invalid choice.")
