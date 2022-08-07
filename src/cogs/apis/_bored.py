from discord.ext import commands
import discord
from discord import app_commands
from src.configs.cmds import boredom
from src.configs.config import CoreConfig
from src.utils.discordUtil import check_perms, perm_req, error




class _boredom(commands.Cog):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    @commands.hybrid_command(name="boredom")
    @app_commands.guilds(CoreConfig.GUILD_ID)
    async def boredom(self, ctx: commands.Context):

        if boredom.ENABLED is False:
            return await error(ctx)
        


async def setup(bot):
    await bot.add_cog(_boredom(bot))
