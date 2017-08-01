"""
Custom super class for all cogs.
"""
from union.core.bot import Union


class Cog(object):
    """
    A custom superclass for all cogs. This provides some valuable things to cog subclasses.
    """
    def __init__(self, bot: Union):
        self.bot = bot

    async def get_config(self, key: str, *, default: Union.no_default):
        """
        Gets a config key for the current cog's config storage.
        """
        return await self.bot.get_config(realm=self.__class__.__name__, key=key,
                                         default=default)

    @classmethod
    def setup(cls, bot: Union):
        """
        Sets up the current cog.
        """
        instance = cls(bot)
        bot.add_cog(instance)
