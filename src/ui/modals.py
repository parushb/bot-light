from discord import ui
import discord
from discord import app_commands
from discord.ext import commands


class EmbedModals:
    def __init__(self, bot):
        self.bot = bot

    class Add_image(ui.Modal, title="Add Image"):
        image_url = discord.ui.TextInput(label="Image URL", placeholder="Image URL ")

        async def on_submit(self, interaction: discord.Interaction):
             return self.image_url

    class MainInput(ui.Modal, title="Embed Data"):
        em_title = ui.TextInput(label="Title", required=False, default="Embed", row=0)
        content = ui.TextInput(label="Content", style=discord.TextStyle.paragraph, row=1)
        footer = ui.TextInput(label="Footer", row=2)
        author = ui.TextInput(label="Author", row=3)

        async def on_submit(self, interaction: discord.Interaction) -> None:
            embed = discord.Embed(title=self.em_title, description=self.content, color=discord.Color.purple())
            embed.set_author(name=self.author)
            embed.set_footer(text=self.footer)
            await interaction.response.send_message(embed=embed, ephemeral=True)



