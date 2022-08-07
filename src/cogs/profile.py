import discord
from typing import Optional
from discord.ext import commands
from discord import app_commands
from src.utils import utils, discordUtil
from src.utils.utils import is_enabled

cfg = utils.return_default_config()
guild = cfg["guild_id"]


class Profile(commands.Cog):
    def __init__(self):
        super().__init__()

    @commands.hybrid_group(fallback="info")
    @app_commands.guilds(guild)
    async def profile(self, ctx: commands.Context, *, user: Optional[discord.Member] = None):
        """
        Return the Profile for a user.
        """
        print(ctx.command)
        if not is_enabled(group="profile"):
            await discordUtil.error(ctx)
        if user is None:
            user = ctx.author

        title, des = discordUtil.get_profile(ctx)
        await discordUtil.send_embed(ctx, title, des, color=discord.Color.blue())

    @profile.command(fallback="avatar")
    @app_commands.guilds(guild)
    async def image(self, ctx: commands.Context, *, user: Optional[discord.Member] = None):
        """
        Get the Profile image for a user.
        """
        if not is_enabled(group="profile"):
            await discordUtil.error(ctx)
            return
        if user is not None:
            ctx.author = user

        img = ctx.author.avatar_url_as(format="png")
        await discordUtil.send_embed(ctx, img=img, color=discord.Color.dark_teal())


async def setup(bot):
    await bot.add_cog(Profile())
