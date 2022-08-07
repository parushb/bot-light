import discord
from discord.ext.commands import Cog

from src.configs.config import CoreConfig
from src.database.user_db import register_guild_users, add_member
from src.main import log

guild = CoreConfig.GUILD_ID


class BaseEvents(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        print(f'{self.bot.user} is ready!')

    @Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

    @Cog.listener()
    async def on_connect(self):
        print(f'{self.bot.user} has connected!')
        await self.bot.tree.sync(guild=discord.Object(id=guild))

    @Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        try:
            role = discord.Role(name="Member")
            if role not in guild.roles:
                await guild.create_role(name="Member", permissions=discord.Permissions.DEFAULT_VALUE())
            else:
                pass
        except discord.Forbidden:
            owner = self.bot.get_user(guild.owner_id)
            await owner.send("Please give me `manager_roles` permission for proper functioning of the Bot")
        users = []
        for member in guild.members:
            users.insert(0, member.id)

        try:
            await register_guild_users(user_list=users, guild_id=guild.id)
        except Exception as E:
            await log(self.bot, f"Registering Guild {guild.id} failed.\n"
                                f"Exception: {E}")

    @Cog.listener()
    async def on_guild_remove(self, guild: discord.Guild):
        await log(self.bot, f"Bot has been removed from {guild.name}, {guild.id} guild.")

    @Cog.listener()
    async def on_member_join(self, member: discord.Member):
        await member.guild.system_channel.send(f"Welcome {member.mention} to the server!")
        await member.send(f"Welcome to {member.guild.name}")
        try:
            await add_member(guild_id=member.guild.id, member_id=member.id)
        except Exception as E:
            await log(self.bot, f"Adding {member.name} with ID {member.id} on guild {member.guild.id} failed."
                                f"Exception: {E}")


async def setup(bot):
    await bot.add_cog(BaseEvents(bot))
