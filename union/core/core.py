import inspect
import io
import sys
import traceback

import discord
from discord.ext import commands

from union.core.cog import Cog
from union.core.context import Context


class Core(Cog):
    """
    Core features of the bot.
    """

    @commands.group(invoke_without_command=True)
    @commands.is_owner()
    async def change(self, ctx: Context):
        """
        Change the looks of the bot.
        """
        await ctx.send(f"\N{RIGHT-POINTING MAGNIFYING GLASS} Please provide a valid subcommand.")

    @change.command(aliases=["username"])
    @commands.is_owner()
    async def name(self, ctx: Context, *, username: commands.clean_content):
        """
        Change the username of the bot.
        """
        await ctx.bot.user.edit(username=username)
        await ctx.send(f"\N{MEMO} Changed username to {username}")

    @change.command(aliases=['playing'])
    @commands.is_owner()
    async def game(self, ctx: Context, *, message: commands.clean_content):
        """
        Change the game of the bot.
        """
        await ctx.bot.change_presence(game=discord.Game(name=message))
        await ctx.send(f"\N{VIDEO GAME} Changed game to {message}")

    @change.command()
    @commands.is_owner()
    async def status(self, ctx: Context, *, status):
        """
        Change the status of the bot.
        """
        await ctx.bot.change_presence(status=status)
        await ctx.send("\N{HEAVY LARGE CIRCLE} Changed status.")

    @change.command(aliases=["avy"])
    @commands.is_owner()
    async def avatar(self, ctx: Context, url: str = None):
        """
        Change the avatar of the bot.

        You can use either attachments or image URLs.
        Providing no attachment or URL will result in a default avatar.
        """
        buffer = io.BytesIO()

        if url is None:
            attachments = ctx.message.attachments
            if attachments:
                await attachments[0].save(buffer)
        else:
            # Since it's owner only right now
            # we give absolute trust to the URL
            async with ctx.bot.session.get(url) as resp:
                buffer.write(await resp.read())

        buffer.seek(0)
        # If the buffer is empty it means no arguments were given by user
        # ergo we should reset the avatar by passing None as the argument
        await ctx.bot.user.edit(avatar=buffer.getvalue() or None)
        await ctx.send("\N{SELFIE} Changed avatar.")

    @commands.command(aliases=['eval'])
    @commands.is_owner()
    async def debug(self, ctx: Context, *, code: str):
        """
        Run code.
        """
        env = {
            "ctx": ctx,
            "bot": ctx.bot,
            "guild": ctx.guild,
            "author": ctx.author,
            "channel": ctx.channel,
            "message": ctx.message
        }
        env.update(sys.modules)
        result = None

        try:
            result = eval(code, env)

            if inspect.isawaitable(result):
                await result
        except:
            await ctx.send(f"```py\n{''.join(traceback.format_exc())}```")
            return

        await ctx.send(f"```py\n{repr(result)}```")

    @commands.command()
    @commands.is_owner()
    async def quit(self, ctx: Context):
        """
        Shut off the bot.
        """
        await ctx.send("\N{LOW BRIGHTNESS SYMBOL} Shutting down...")
        await ctx.bot.logout()


setup = Core.setup
