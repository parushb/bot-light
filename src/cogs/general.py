from typing import Optional

import discord
from discord.ext import commands
from discord import app_commands
from src.utils.utils import return_default_config

cfg = return_default_config()
guild_id: int = cfg['guild_id']


class MyCog(commands.Cog):
    def __init__(self):
        super().__init__()



async def setup(bot):
    await bot.add_cog(MyCog())
