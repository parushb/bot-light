from typing import Optional

import discord
from discord.ext import commands
from discord import app_commands
from src.utils.discordUtil import check_perms, send_embed, error, is_enabled
from src.ui.buttons import BanConfirm, UnBanConfirm
from src.configs.config import CoreConfig as cfg
from src.configs.cmds import Ban, UnBan
from src.main import logger


class _Ban(commands.Cog):
    def __init__(self):
        super().__init__()

    @commands.hybrid_command(name="ban", pass_context=True)
    @app_commands.guilds(cfg.GUILD_ID)
    async def _ban(self, ctx: commands.Context, user: discord.Member, reason: Optional[str]):
        if Ban.ENABLED is False:
            await error(ctx)
            return

        view = BanConfirm(ctx, user)
        logger().debug(user)
        await send_embed(ctx, title="Member Ban Confirmation",
                         description=f"Are you sure that you want to Ban {user.name}?", view=view)
        await view.wait()
        if view.value is None:
            await ctx.send("Timed out")
        view.stop()

    @commands.hybrid_command(name="unban", pass_context=True)
    @app_commands.guilds(cfg.GUILD_ID)
    @app_commands.describe(user="User to unban, Pass the full user ID with the user discriminator")
    async def _unban(self, ctx: commands.Context, user: str, reason: Optional[str]):
        if not is_enabled("unban"):
            await error(ctx)
            return

         # unban a user
        view = UnBanConfirm(ctx)
        await send_embed(ctx, title="Member UnBan Confirmation",
                         description=f"Are you sure that you want to UnBan {user}?", view=view)
        await view.wait()

        if view.value:
            # await ctx.guild.unban(user, reason=reason)
            await send_embed(ctx, title="Member UnBan", description=f"{user} has been UnBanned by {ctx.author.name}\n"
                                                                    f"**Reason**: {reason}")
        elif view.value is False:
            await ctx.send("Cancelled")
        view.stop()


async def setup(bot):
    await bot.add_cog(_Ban())
