import discord
from discord.ext import commands
import json
import requests
from discord import app_commands
from src.configs.config import CoreConfig
from src.utils.discordUtil import check_perms, perm_req, error, send_embed


def get_dict(word):
    response = requests.get(f"https://api.urbandictionary.com/v0/define?term={word}")
    meaning = json.loads(response.text)['list'][0]
    meaning = f"Word: {meaning['word']}\n"\
              f"**Definition** : {meaning['definition']}"
    return meaning


class _dictionary(commands.Cog):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    @commands.hybrid_command(name="dictionary")
    @app_commands.guilds(CoreConfig.GUILD_ID)
    async def dictionary(self, ctx: commands.Context, word: str):
        await send_embed(ctx, title="Dictionary", description=get_dict(word), color=discord.Color.teal())


async def setup(bot):
    await bot.add_cog(_dictionary(bot))
