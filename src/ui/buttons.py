import discord
from discord.ui import Button
from src.utils.discordUtil import create_embed

class BanConfirm(discord.ui.View):

    def __init__(self, ctx, user):
        super().__init__()
        self.value = None
        self.ctx = ctx
        self.user = user

    @discord.ui.button(label="Ban", emoji="🟥", style=discord.ButtonStyle.danger, custom_id="ban_confirm")
    async def confirm(self, interaction: discord.Interaction, button: Button):
        if interaction.user.id == self.ctx.author.id:
            self.value = True
            embed = await create_embed("Member Banned", f"**{self.user}** has been kicked by **{self.ctx.author}**")
            await interaction.response.send_message(embed=embed)
            self.stop()
        else:
            # send a message in the channel
            await interaction.response.send_message(f"That interaction is not yours!", ephemeral=True)

    @discord.ui.button(label="Cancel", emoji="❎", style=discord.ButtonStyle.gray, custom_id="ban_cancel")
    async def cancel(self, interaction: discord.Interaction, button: Button):
        if interaction.user.id == self.ctx.author.id:
            self.value = False
            embed = await create_embed("Member Ban cancelled", f"**{self.user} wasn't Banned this time**")
            await interaction.response.send_message(embed=embed)
            self.stop()
        else:
            # send a message in the channel
            await interaction.response.send_message("That interaction is not yours!", ephemeral=True)


class UnBanConfirm(discord.ui.View):

    def __init__(self, ctx):
        super().__init__()
        self.value = None
        self.ctx = ctx

    @discord.ui.button(label="UnBan", style=discord.ButtonStyle.danger)
    async def confirm(self, interaction: discord.Interaction, button: Button):
        if interaction.user.id == self.ctx.author.id:
            self.value = True
            self.stop()
        else:
            # send a message in the channel
            await interaction.response.send_message("That interaction is not yours!", ephemeral=True)

    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.gray)
    async def cancel(self, interaction: discord.Interaction, button: Button):
        if interaction.user.id == self.ctx.author.id:
            self.value = False
            self.stop()
        else:
            # send a message in the channel
            await interaction.response.send_message("That interaction is not yours!", ephemeral=True)


class KickConfirm(discord.ui.View):
    def __init__(self, ctx, user: discord.Member, reason: str):
        super().__init__()
        self.value = None
        self.ctx = ctx
        self.user = user
        self.reason = reason

    @discord.ui.button(label="Kick", style=discord.ButtonStyle.danger)
    async def confirm(self, interaction: discord.Interaction, button: Button):
        if interaction.user.id == self.ctx.author.id:
            self.value = True
            await interaction.guild.kick(user=self.user, reason=self.reason)
            embed = await create_embed("Member Kick", f"**{self.user}** has been kicked by **{self.ctx.author}**")
            await interaction.response.send_message(embed=embed)
            self.stop()
        else:
            # send a message in the channel
            await interaction.response.send_message("That interaction is not yours!", ephemeral=True)

    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.gray)
    async def cancel(self, interaction: discord.Interaction, button: Button):
        if interaction.user.id == self.ctx.author.id:
            self.value = False
            embed = await create_embed("kick cancelled", f"**{self.user}** has not been kicked")
            await interaction.response.send_message(embed=embed)
            self.stop()
        else:
            # send a message in the channel
            await interaction.response.send_message("That interaction is not yours!", ephemeral=True)
