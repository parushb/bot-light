import discord
from discord.ext import commands
from discord import app_commands
from src.utils.utils import return_default_config, return_cmd_config, is_enabled
from src.utils.discordUtil import sayConfirm, error, check_perms, EmbedTextParams
from src.configs.cmds import Say
from src.configs.config import CoreConfig


class Embed(commands.Cog):
    def __init__(self):
        super().__init__()

    @commands.hybrid_command(name="say", aliases=Say.ALIASES)
    @app_commands.guilds(CoreConfig.GUILD_ID)
    async def _say(self, ctx: commands.Context, content: str):
        if not is_enabled("say"):
            return await error(ctx)

        embed = None
        add_embed = True
        if add_embed:
            embed = discord.Embed()

            modal = EmbedTextParams(title="Embed parameters")
            await ctx.interaction.response.send_modal(modal)
            if await modal.wait(): return

            if modal.titleTxt.value:
                embed.title = modal.titleTxt.value
            if modal.authorName.value:
                embed.set_author(name=modal.authorName.value, icon_url=None)
            if modal.desc.value:
                embed.description = modal.desc.value
            if modal.footerText.value:
                embed.set_footer(text=modal.footerText.value, icon_url=None)
            if modal.colour.value:
                if modal.colour.value.lower() == "random":
                    embed.colour = discord.Colour.random()
                else:
                    embed.colour = discord.Colour(int(modal.colour.value, base=16))
            else:
                embed.colour = None

        await sayConfirm(ctx.interaction, content, embed)


async def setup(bot):
    await bot.add_cog(Embed())
