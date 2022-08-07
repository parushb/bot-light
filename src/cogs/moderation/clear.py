from discord.ext import commands
from discord import app_commands
from src.utils.discordUtil import check_perms, error, perm_req

from src.configs.config import CoreConfig as Cfg
from src.configs.cmds import Clear as Cmd
from typing import Optional


class Clear(commands.Cog):
    def __init__(self):
        super().__init__()

    @commands.hybrid_command(name="clear")
    @app_commands.guilds(Cfg.GUILD_ID)
    async def clear(self, ctx: commands.Context, amount: Optional[int] = None):
        # Write Command Code here

        if amount is None:
            amount = 20

        await ctx.channel.purge(limit=amount)
        await ctx.send(f"{amount} messages have been deleted.", ephemeral=True)


async def setup(bot):
    await bot.add_cog(Clear())
