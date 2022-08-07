from discord.ext import commands
import discord
from discord import app_commands
from src.utils.utils import return_default_config, return_cmd_config, is_enabled
from src.utils.discordUtil import check_perms, error, perm_req, send_embed
from src.ui.buttons import KickConfirm

config = return_default_config()
cmd_config = return_cmd_config()


class Kick(commands.Cog):
    def __init__(self):
        super().__init__()

    @commands.hybrid_command(name="kick", aliases=cmd_config["kick"]["aliases"])
    @app_commands.guilds(config["guild_id"])
    @app_commands.describe(member="The member to Kick",
                           reason="The reason for the kick(visible in audit log), optional")
    async def kick(self, ctx: commands.Context, member: discord.Member, reason: str = None):
        # Write Command Code here
        if member == ctx.author:
            await ctx.send("You can't kick yourself.", ephemeral=True)
            return
        elif member.top_role.position > ctx.author.top_role.position:
            await send_embed(ctx, "You can't kick someone with a higher role than you.")
            return

        view = KickConfirm(ctx, member, reason)
        await send_embed(ctx, description=f"Are you sure you want to kick {member.name}?", view=view)


async def setup(bot):
    await bot.add_cog(Kick())
