from discord.ext import commands
from discord import app_commands
from src.utils.discordUtil import check_perms, send_embed
from src.configs.config import CoreConfig


class _Prefix(commands.Cog):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    @commands.hybrid_command(name="prefix")
    @app_commands.guilds(CoreConfig.GUILD_ID)
    async def prefix(self, ctx: commands.Context, new_prefix: str):

        if len(new_prefix) > 5:
            return await ctx.send("You cannot set prefix more than 5 letters long", ephemeral=True)

        await self.bot.db.execute(f"""
            UPDATE guild_config SET prefix = {new_prefix} WHERE guild_id = {ctx.guild.id}
        """)
        await send_embed(ctx, title="Prefix Change", description=f"The new prefix is now set to")
        return


async def setup(bot):
    await bot.add_cog(_Prefix(bot))
