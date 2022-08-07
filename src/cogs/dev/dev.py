from typing import Optional, Literal

import discord
from discord import Object
from discord.ext import commands
from discord.ext.commands import Greedy

from configs.config import CoreConfig
from src.database.user_db import register_guild_users
import asyncio

from utils.discordUtil import only_dev


class dev(commands.Cog):

    def __init__(self):
        super().__init__()

    @commands.command()
    @only_dev
    async def load_db(self, ctx: commands.Context):
        await ctx.send("Loading database...")
        users = []
        for member in ctx.guild.members:
            users.append(member.id)

        asyncio.get_event_loop().run_until_complete(register_guild_users(user_list=users, guild_id=ctx.guild.id))
        await ctx.send("Database loaded!")

    @commands.command(name="reload")
    @only_dev
    async def reload(self, ctx: commands.Context):
        await ctx.send("You are a dev")

    @commands.command()
    @commands.is_owner()
    async def sync(self, ctx: commands.Context, guilds: Greedy[Object], spec: Optional[Literal["~", "*"]] = None) -> None:
        if not guilds:
            if spec == "~":
                fmt = await ctx.bot.tree.sync(guild=ctx.guild)
            elif spec == "*": 
                ctx.bot.tree.copy_global_to(guild=ctx.guild)
                fmt = await ctx.bot.tree.sync(guild=ctx.guild)
            else:
                fmt = await ctx.bot.tree.sync()

            await ctx.send(
                f"Synced {len(fmt)} commands {'globally' if spec is None else 'to the current guild.'}"
            )
            return

        fmt = 0
        for guild in guilds:
            try:
                await ctx.bot.tree.sync(guild=guild)
            except discord.HTTPException:
                pass
            else:
                fmt += 1

        await ctx.send(f"Synced the tree to {fmt}/{len(guilds)} guilds.")


async def setup(bot):
    await bot.add_cog(dev())

