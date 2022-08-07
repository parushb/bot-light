# Code For the command /meme <term> , !meme <term>

import random

from discord import app_commands
from discord.ext import commands
from typing import Optional

from src.utils.utils import return_default_config, return_cmd_config, get_meme

config = return_default_config()
cmdConfig = return_cmd_config()

guild = config['guild_id']


class Meme(commands.Cog):
    def __init__(self):
        super().__init__()

    @commands.hybrid_command(name="meme")
    @app_commands.guilds(guild)
    async def _meme(self, ctx: commands.Context, term: Optional[str]):

        if term is None:
            term = cmdConfig["meme"]["terms"][random.randint(

                0, len(cmdConfig["meme"]["terms"]) - 1)]
            meme = get_meme(term)
            for i in range(len(meme['results'])):
                url = meme['results'][i]['media'][0]['gif']['url']
                await ctx.send(url)
            return

        else:
            meme = get_meme(term)
            for i in range(len(meme['results'])):
                url = meme['results'][i]['media'][0]['gif']['url']
                await ctx.send(url)
            return


async def setup(bot):
    await bot.add_cog(Meme())
