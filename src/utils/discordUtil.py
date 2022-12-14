from typing import Optional

import discord
from discord import Interaction, ButtonStyle, Embed, TextStyle, Colour, SelectOption
from discord.ext import commands
from discord.ui import View, Modal, TextInput, Button, Select
from discord.utils import MISSING
from src.configs.config import Dev, CoreConfig
from src.main import logger

EMPTY_IMAGE = "https://cdn.discordapp.com/attachments/700683544103747594/979495873190969424/empty.png"
ZWSP = "​"


def only_dev(func):
    async def inner(*args, **kwargs):
        ctx = args[1]
        if ctx.author.id in Dev.developers:
            return await func(*args, **kwargs)

    return inner


def embed_empty(embed: Embed) -> bool:
    return not any((embed.fields, embed.title, embed.author.name if embed.author else None,
                    embed.author.icon_url if embed.author else None, embed.description,
                    embed.footer.text if embed.footer else None, embed.footer.icon_url if embed.footer else None))


async def error(ctx: commands.Context):
    await ctx.send(f'{ctx.command.name} is disabled or the command is currently under development.')


async def perm_req(ctx: commands.Context, *perms):
    await send_embed(ctx, title="Permissions Required",
                     description=f"You need the following permissions to run this command: {perms}",
                     color=0xff3636)


async def send_embed(ctx: commands.Context,
                     title: str = None,
                     description: str = None,
                     color: int = 0x00ff00,
                     img:str =None,
                     view: discord.ui.View = None):
    """
    Sends an embed message to the channel the command was invoked in.
    """

    embed = discord.Embed(title=title, description=description, color=color)
    if ctx.author.avatar.url is None:
        embed.set_author(name=ctx.author.name)
    else:
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
    if img is not None:
        embed.set_image(url=img)

    if view is not None:
        await ctx.send(embed=embed, view=view)
        return
    await ctx.send(embed=embed)
    return


async def create_embed(
        title: str = None,
        description: str = None,
        color: int = 0x00ff00,
        img: str = None) -> discord.Embed:
    """
    Sends an embed message to the channel the command was invoked in.
    """

    embed = discord.Embed(title=title, description=description, color=color)
    if img is not None:
        embed.set_image(url=img)

    return embed


# A better Embed Maker

def get_profile(ctx: commands.Context):
    title = f"{ctx.author.name}#{ctx.author.discriminator}'s Profile"
    description = f"**Username:** {ctx.author.name}\n" \
                  f"**Discriminator:** {ctx.author.discriminator}\n" \
                  f"**ID:** {ctx.author.id}\n" \
                  f"**Created At:** {ctx.author.created_at}\n*" \
                  f"*Joined At:** {ctx.author.joined_at}"
    return title, description


def is_enabled(func):                   # This decorator doesn't work.
    async def inner(*args, **kwargs):
        ctx = args[1]
        if ctx.command.name not in CoreConfig.enabled_commands:
            await ctx.send(f"The Command `{ctx.command.name}` is currently disabled."
                            f" I am sorry for this, but this is usually done when some new features"
                            f" or changes to the command are being done 😉", ephemeral=True)
            return False
        else: return True
    return commands.check(inner)

def check_perms(**perms):

    async def predicate(ctx):
        if ctx.guild is None:
            return False
        invalid = set(perms) - set(discord.Permissions.VALID_FLAGS)
        if invalid:
            await ctx.send("An error occurred, invalid permissions were passed.")

        channel = ctx.channel
        permissions = channel.permissions_for(ctx.author)
        missing = [perm for perm, value in perms.items() if getattr(permissions, perm) != value]
        if missing:
            await send_embed(ctx, title="Permissions Required",
                             description=f"You don't have sufficient permissions to run the command",
                             color=0xff3636)
        return missing
    return commands.check(predicate)


class EmbedTextParams(Modal):
    authorName = TextInput(label="Author name", required=False, max_length=256)
    titleTxt = TextInput(label="Title", required=False, max_length=256)
    desc = TextInput(label="Description", required=False, style=TextStyle.paragraph, max_length=4000)
    footerText = TextInput(label="Footer text", required=False, max_length=2048)
    colour = TextInput(label="Colour (hex or RANDOM)", required=False, max_length=8)

    def __init__(self, *, title: str = MISSING, timeout: Optional[float] = None, custom_id: str = MISSING,
                 currentEmbed: Embed = None):
        super().__init__(title=title, timeout=timeout, custom_id=custom_id)
        if currentEmbed is not None:
            self.titleTxt.default = currentEmbed.title or ""
            self.authorName.default = (currentEmbed.author.name or "") if currentEmbed.author is not None else ""
            self.desc.default = currentEmbed.description or ""
            self.footerText.default = (currentEmbed.footer.text or "") if currentEmbed.footer is not None else ""
            self.colour.default = hex(currentEmbed.colour.value) if currentEmbed.colour is not None else ""

    async def on_submit(self, interaction: Interaction) -> None:
        await interaction.response.defer(thinking=False)


class EmbedImageParams(Modal):
    authorIcon = TextInput(label="Author icon", required=False, max_length=4000)
    thumb = TextInput(label="Thumbnail", required=False, max_length=4000)
    img = TextInput(label="Image", required=False, max_length=4000)
    footerIcon = TextInput(label="Footer icon", required=False, max_length=4000)

    def __init__(self, *, title: str = MISSING, timeout: Optional[float] = None, custom_id: str = MISSING,
                 currentEmbed: Embed = None):
        super().__init__(title=title, timeout=timeout, custom_id=custom_id)
        if currentEmbed is not None:
            self.authorIcon.default = (currentEmbed.author.icon_url or "") if currentEmbed.author is not None else ""
            self.thumb.default = (currentEmbed.thumbnail.url or "") if currentEmbed.thumbnail is not None else ""
            self.img.default = (currentEmbed.image.url or "") if currentEmbed.image is not None else ""
            self.footerIcon.default = (currentEmbed.footer.icon_url or "") if currentEmbed.footer is not None else ""

    async def on_submit(self, interaction: Interaction) -> None:
        await interaction.response.defer(thinking=False)


class EmbedFieldParams(Modal):
    fieldName = TextInput(label="Feld name", required=False)
    fieldValue = TextInput(label="Field value", required=False, style=TextStyle.paragraph)
    fieldInline = TextInput(label="Inline? (y/n)", required=False, max_length=1, placeholder="n")

    async def on_submit(self, interaction: Interaction) -> None:
        await interaction.response.defer(thinking=False)


async def sayConfirm(originalInteraction: Interaction, content: str, embed: Optional[Embed]):
    view = View()

    async def send(interaction: Interaction):
        await interaction.response.edit_message(content="sent!", view=None)
        if embed_empty(embed):
            embed.description = ZWSP
        await interaction.channel.send(content=content, embed=embed)
        view.stop()

    async def cancel(interaction: Interaction):
        await interaction.response.edit_message(view=None)
        view.stop()

    async def addField(interaction: Interaction):
        if len(embed.fields) == 25:
            await interaction.response.send_message(
                f"🇽 Maximum number of fields reached. Please remove one, or edit an existing field.")
            return

        modal = EmbedFieldParams(title="Field Parameters")

        await interaction.response.send_modal(modal)
        if await modal.wait(): view.stop()

        embed.add_field(name=modal.fieldName.value or ZWSP, value=modal.fieldValue.value or ZWSP,
                        inline=modal.fieldInline.value.lower() == "y")
        if embed_empty(embed):
            emptyEmbed = True
            embed.description = ZWSP
        else:
            emptyEmbed = False
        await interaction.edit_original_message(embed=embed)
        if emptyEmbed:
            embed.description = None

    async def removeField(interaction: Interaction):
        if not embed.fields:
            await interaction.response.send_message("The embed has no fields!", ephemeral=True)
            return

        async def stopSelectorView(interaction: Interaction):
            selectedFieldIndices = sorted([int(i) for i in fieldSelector.values], reverse=True)
            for i in selectedFieldIndices:
                embed.remove_field(i)

            if embed_empty(embed):
                emptyEmbed = True
                embed.description = ZWSP
            else:
                emptyEmbed = False
            view.remove_item(fieldSelector)

            for c in view.children:
                if isinstance(c, Button):
                    c.disabled = False

            await interaction.response.edit_message(embed=embed, view=view)
            if emptyEmbed:
                embed.description = None

        for c in view.children:
            if isinstance(c, Button):
                c.disabled = True

        fieldSelector = Select(options=[SelectOption(label=f"{i + 1}. {field.name}", value=str(i)) for i, field in
                                        enumerate(embed.fields)], max_values=min(len(embed.fields), 25))
        fieldSelector.callback = stopSelectorView
        view.add_item(fieldSelector)

        await interaction.response.edit_message(view=view)

    async def editField(interaction: Interaction):
        if not embed.fields:
            await interaction.response.send_message("The embed has no fields!", ephemeral=True)
            return

        fieldSelector = Select(options=[SelectOption(label=f"{i + 1}. {field.name}", value=str(i)) for i, field in
                                        enumerate(embed.fields)], max_values=1)

        async def stopSelectorView(interaction: Interaction):
            selectedFieldIndex = int(fieldSelector.values[0])
            field = embed.fields[selectedFieldIndex]

            modal = EmbedFieldParams(title="Field Parameters")
            if field.name != ZWSP:
                modal.fieldName.default = field.name
            if field.value != ZWSP:
                modal.fieldValue.default = field.value
            modal.fieldInline.default = "y" if field.inline else "n"

            await interaction.response.send_modal(modal)
            if await modal.wait(): view.stop()

            for c in view.children:
                if isinstance(c, Button):
                    c.disabled = False

            view.remove_item(fieldSelector)

            embed.set_field_at(selectedFieldIndex, name=modal.fieldName.value or ZWSP,
                               value=modal.fieldValue.value or ZWSP, inline=modal.fieldInline.value.lower() == "y")
            if embed_empty(embed):
                emptyEmbed = True
                embed.description = ZWSP
            else:
                emptyEmbed = False
            await interaction.edit_original_message(embed=embed, view=view)
            if emptyEmbed:
                embed.description = None

        for c in view.children:
            if isinstance(c, Button):
                c.disabled = True

        fieldSelector.callback = stopSelectorView
        view.add_item(fieldSelector)

        await interaction.response.edit_message(view=view)

    async def editEmbedText(interaction: Interaction):
        modal = EmbedTextParams(title="Embed Parameters", currentEmbed=embed)

        await interaction.response.send_modal(modal)
        if await modal.wait(): view.stop()

        if modal.titleTxt.value:
            embed.title = modal.titleTxt.value
        else:
            embed.title = None

        authorIcon = (embed.author.icon_url or "") if embed.author is not None else ""
        if modal.authorName.value:
            embed.set_author(name=modal.authorName.value, icon_url=authorIcon or None)
        else:
            if authorIcon:
                embed.set_author(name=ZWSP, icon_url=authorIcon)
            else:
                embed.remove_author()

        if modal.desc.value:
            embed.description = modal.desc.value
        else:
            embed.description = None

        footerIcon = (embed.footer.icon_url or "") if embed.footer is not None else ""
        if modal.footerText.value:
            embed.set_footer(text=modal.footerText.value, icon_url=footerIcon or None)
        else:
            if footerIcon:
                embed.set_footer(text=ZWSP, icon_url=footerIcon)
            else:
                embed.remove_footer()

        if modal.colour.value:
            if modal.colour.value.lower() == "random":
                embed.colour = Colour.random()
            else:
                embed.colour = Colour(int(modal.colour.value, base=16))
        else:
            embed.colour = None

        if embed_empty(embed):
            emptyEmbed = True
            embed.description = ZWSP
        else:
            emptyEmbed = False
        await interaction.edit_original_message(embed=embed)
        if emptyEmbed:
            embed.description = None

    async def editEmbedImages(interaction: Interaction):
        modal = EmbedImageParams(title="Embed parameters", currentEmbed=embed)
        await interaction.response.send_modal(modal)
        if await modal.wait(): return

        authorName = (
            "" if embed.author.name in (None, ZWSP) else embed.author.name) if embed.author is not None else ""
        if modal.authorIcon.value:
            embed.set_author(name=authorName or ZWSP, icon_url=modal.authorIcon)
        else:
            if authorName:
                embed.set_author(name=authorName, icon_url=None)
            else:
                embed.remove_author()

        embed.set_thumbnail(url=modal.thumb.value or None)
        embed.set_image(url=modal.img.value or None)

        footerText = (
            "" if embed.footer.text in (None, ZWSP) else embed.footer.text) if embed.footer is not None else ""
        if modal.footerIcon.value:
            embed.set_footer(text=footerText or ZWSP, icon_url=modal.footerIcon)
        else:
            if footerText:
                embed.set_footer(text=footerText, icon_url=None)
            else:
                embed.remove_footer()

        if embed_empty(embed):
            emptyEmbed = True
            embed.description = ZWSP
        else:
            emptyEmbed = False
        await interaction.edit_original_message(embed=embed)
        if emptyEmbed:
            embed.description = None

    confirmButton = Button(style=ButtonStyle.green, label="send", row=0 if embed is None else 2)
    confirmButton.callback = send
    cancelButton = Button(style=ButtonStyle.red, label="cancel", row=0 if embed is None else 2)
    cancelButton.callback = cancel
    view.add_item(cancelButton).add_item(confirmButton)
    if embed is not None:
        editEmbedTextButton = Button(style=ButtonStyle.blurple, label="edit embed text", row=0)
        editEmbedTextButton.callback = editEmbedText
        view.add_item(editEmbedTextButton)

        editEmbedImagesButton = Button(style=ButtonStyle.blurple, label="edit embed images", row=0)
        editEmbedImagesButton.callback = editEmbedImages
        view.add_item(editEmbedImagesButton)

        addFieldButton = Button(style=ButtonStyle.blurple, label="add embed field", row=1)
        addFieldButton.callback = addField
        view.add_item(addFieldButton)

        removeFieldButton = Button(style=ButtonStyle.blurple, label="remove embed field", row=1)
        removeFieldButton.callback = removeField
        view.add_item(removeFieldButton)

        editFieldButton = Button(style=ButtonStyle.blurple, label="edit embed field", row=1)
        editFieldButton.callback = editField
        view.add_item(editFieldButton)

    if embed is not None:
        if embed_empty(embed):
            emptyEmbed = True
            embed.description = ZWSP
        else:
            emptyEmbed = False
    await originalInteraction.followup.send(content=content, embed=embed, ephemeral=True, view=view)
    if embed is not None and emptyEmbed:
        embed.description = None
