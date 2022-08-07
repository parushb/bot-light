import discord
from discord.ext import commands

from src.utils.utils import return_default_config, return_cmd_config, is_enabled
from src.utils.discordUtil import send_embed, check_perms, perm_req, error
from discord import app_commands

config = return_default_config()
cmd_config = return_cmd_config()


class Mute(commands.Cog):
    def __init__(self):
        super().__init__()

    @commands.hybrid_command(name="mute", aliases=cmd_config["mute"]["aliases"], pass_context=True)
    @app_commands.guilds(config["guild_id"])
    @app_commands.describe(member="The member to mute",
                           reason="The reason for the mute")
    async def mute(self, ctx: commands.Context, member: discord.Member, *, reason: str = None):
        """Mutes a Member"""

        if member == ctx.author:
            await ctx.send(f"{ctx.author.mention} You can't mute yourself!")
            return

        role = discord.utils.get(ctx.guild.roles, name="Muted")

        if role is None:

            # make the role
            role = await ctx.guild.create_role(name="Muted", permissions=discord.Permissions.none(), color=discord.Color.dark_grey())
            # Editing the role permissions to disable sending messages
            for channel in ctx.guild.text_channels:
                await channel.set_permissions(role, send_messages=False, add_reactions=False)
            for channel in ctx.guild.voice_channels:
                await channel.set_permissions(role, speak=False, connect=False)

        if role in member.roles:
            await ctx.send(f"{ctx.author.mention} That member is already muted!")
            return
        await member.add_roles(role)
        await send_embed(ctx, title="Mute", description=f"{member.mention} has been muted", color=0x17a8fc)
        return

    # Command: UNMUTE

    @commands.hybrid_command(name="unmute", aliases=cmd_config["unmute"]["aliases"], pass_context=True)
    @app_commands.guilds(config["guild_id"])
    @app_commands.describe(member="The member to unmute")
    async def unmute(self, ctx: commands.Context, member: discord.Member):
        """Unmutes a member"""

        if member == ctx.author:
            await ctx.send(f"{ctx.author.mention} You can't unmute yourself!")
            return

        role = discord.utils.get(ctx.guild.roles, name="Muted")

        if role is None:

            # make the role
            role = await ctx.guild.create_role(name="Muted", permissions=discord.Permissions.none(), color=discord.Color.dark_grey())
            # Editing the role permissions to disable sending messages
            for channel in ctx.guild.text_channels:
                await channel.set_permissions(role, send_messages=False, add_reactions=False)
            for channel in ctx.guild.voice_channels:
                await channel.set_permissions(role, speak=False, connect=False)

        if role not in member.roles:
            await ctx.send(f"{ctx.author.mention} That member is already unmuted!")
            return
        await member.remove_roles(role)

        await send_embed(ctx, title="Mute", description=f"{member.mention} has been unmuted", color=0x17a8fc)
        return


async def setup(bot):
    await bot.add_cog(Mute())
